from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d

from .optics import PhysicalModelConfig, physical_spectrum, unpolarized_reflectance


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
WAVELENGTH_NM = np.linspace(420.0, 780.0, 361)
MODEL_CONFIG = PhysicalModelConfig(
    angle_deg=8.0,
    spectral_blur_sigma_nm=0.6,
    model="tmm",
    dispersion=True,
)


@dataclass(frozen=True)
class NKTable:
    wavelength_nm: np.ndarray
    n: np.ndarray
    k: np.ndarray


def load_nk(path: Path) -> NKTable:
    with path.open("r", encoding="ascii", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["wavelength_nm", "n", "k"]:
            raise ValueError(f"Unexpected n,k schema: {path}")
        rows = [(float(row["wavelength_nm"]), float(row["n"]), float(row["k"])) for row in reader]
    values = np.asarray(rows, dtype=float)
    if values.ndim != 2 or values.shape[1] != 3 or not np.isfinite(values).all():
        raise ValueError(f"Invalid n,k table: {path}")
    if not np.all(np.diff(values[:, 0]) > 0.0) or np.any(values[:, 2] < 0.0):
        raise ValueError(f"Invalid wavelength order or negative k: {path}")
    return NKTable(values[:, 0], values[:, 1], values[:, 2])


def interpolate_complex_index(table: NKTable, wavelength_nm: np.ndarray) -> np.ndarray:
    query = np.asarray(wavelength_nm, dtype=float)
    if query.min() < table.wavelength_nm[0] or query.max() > table.wavelength_nm[-1]:
        raise ValueError("Optical-constant extrapolation is forbidden")
    n_value = np.interp(query, table.wavelength_nm, table.n)
    k_value = np.interp(query, table.wavelength_nm, table.k)
    return n_value + 1j * k_value


@lru_cache(maxsize=1)
def material_sources() -> dict[str, dict[str, object]]:
    path = PACKAGE_ROOT / "configs" / "material_sources.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=16)
def _table(relative_path: str) -> NKTable:
    return load_nk(PACKAGE_ROOT / relative_path)


@lru_cache(maxsize=3)
def make_material_spectrum(material_id: str):
    if material_id == "A":
        @lru_cache(maxsize=25000)
        def analytic_spectrum(thickness_nm: float) -> np.ndarray:
            return physical_spectrum(WAVELENGTH_NM, float(thickness_nm), MODEL_CONFIG)

        return analytic_spectrum
    source = material_sources().get(material_id)
    if source is None or source.get("mode") != "normalized_nk_tables":
        raise ValueError(f"Unknown material_id: {material_id}")
    wavelength_nm = WAVELENGTH_NM
    n_film = interpolate_complex_index(_table(str(source["film_table"])), wavelength_nm)
    n_substrate = interpolate_complex_index(_table(str(source["substrate_table"])), wavelength_nm)
    config = MODEL_CONFIG

    @lru_cache(maxsize=25000)
    def spectrum(thickness_nm: float) -> np.ndarray:
        reflectance = unpolarized_reflectance(
            config.model,
            wavelength_nm,
            float(thickness_nm),
            1.0,
            n_film,
            n_substrate,
            config.angle_deg,
        )
        if config.spectral_blur_sigma_nm > 0.0:
            spacing_nm = float(np.median(np.diff(wavelength_nm)))
            reflectance = gaussian_filter1d(
                reflectance,
                config.spectral_blur_sigma_nm / spacing_nm,
                mode="nearest",
            )
        result = np.asarray(reflectance, dtype=float)
        if result.shape != wavelength_nm.shape or not np.isfinite(result).all():
            raise ValueError("Generated material spectrum is invalid")
        return result

    return spectrum
