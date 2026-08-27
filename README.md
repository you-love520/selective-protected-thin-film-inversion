# Selective Protected Refinement for Thin-Film Thickness Inversion

This repository contains the core algorithm implementation, frozen configuration, manuscript-aligned summary tables, and verification scripts supporting the Stage33 / Final A+B version of the method.

## Manuscript result identity

- Development seed: `20260426`
- Independent-validation seed: `20260508`
- Independent-validation design: `3 materials x 3 thicknesses x 4 contamination scenarios x 200 observations = 7200 observations`
- Robust anchor: E3 robust multibasin profile
- Final method: selective protected refinement, reported as Final A+B
- Adaptive protection: `eta2 = C2`
- B-routing thresholds: maximum relative basin gap `5.0`; minimum local-identifiability score `0.82`

## Headline validation results

| Quantity | Value |
|---|---:|
| E3 mean absolute error | 0.223465 nm |
| Final A+B mean absolute error | 0.194634 nm |
| A-only accepted refinements | 2976 |
| A-only improved / harmed | 2053 / 923 |
| Final A+B accepted refinements | 2410 |
| Final A+B improved / harmed | 1915 / 495 |
| Exact E3 fallback | 4790 |
| Mean Final A+B minus E3 | -0.028831 nm |
| Mean Final A+B minus A-only | -0.021967 nm |

## Repository layout

```text
src/stage33_anchor/     Robust-anchor and forward-model source modules
src/final_ab/           Selective protected-refinement source modules
configs/                Frozen Final A+B parameters and routing thresholds
data/optical_constants/ Frozen optical-constant tables used by materials B and C
tables/                 Manuscript table source CSV files
figures/                Generated figures
analysis/               Verification, table-building, figure-building, and threshold-selection scripts
environment/            Python dependency lock
provenance/             Checksum manifest
```

## Software environment and dependencies

The implementation was prepared for Python 3.12. The public package specifies seven direct Python dependencies for numerical optimization, structured-data processing, runtime monitoring, and visualization.

### Direct dependencies

| Package | Version | Role in the computational workflow |
|---|---:|---|
| NumPy | 2.5.1 | Array operations, numerical linear algebra, spectrum handling, and seeded random-number generation |
| SciPy | 1.18.0 | Bounded optimization, scalar minimization, linear least squares, and Gaussian spectral-response filtering |
| pandas | 2.2.2 | Tabular result processing and CSV-based analysis |
| Matplotlib | 3.9.1 | Scientific plotting and vector/raster figure export |
| PyArrow | 17.0.0 | Columnar data exchange and Parquet-compatible data handling |
| psutil | 7.2.2 | Runtime and system-resource monitoring |
| Polars | 1.42.1 | Efficient processing of larger structured result tables |

The core optical model, robust multibasin anchor, and protected-refinement implementation primarily depend on NumPy and SciPy. The remaining packages support result-table processing, runtime analysis, columnar data handling, and scientific visualization.

### Installation

Create an isolated Python environment before installing the dependencies.

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The pinned dependency list is provided in:

```text
requirements.txt
environment/requirements-lock.txt
```

Using the pinned versions is recommended when reproducing the reported software environment.


## Threshold-selection reproduction

Run:

```bash
python analysis/select_b_thresholds.py --input configs/THRESHOLD_SELECTION_INPUT.json --output analysis/THRESHOLD_SELECTION_REPRODUCED_CHECK.json
```

This reproduces the deterministic B-routing threshold selection from the development grid.

## License

The original source code and documentation in this repository are released
under the MIT License. See `LICENSE` for details.

Third-party optical-property data and published dispersion parameters retain
their original attribution and applicable terms. See
`THIRD_PARTY_NOTICES.md`.

## Citation

Citation metadata for this software release are provided in `CITATION.cff`.

## Third-party data and attribution

Selected optical-property data used by the forward models originate from
KLA/Filmetrics database records and the Zenodo dataset
10.5281/zenodo.15055400. Detailed provenance and attribution are provided in
`THIRD_PARTY_NOTICES.md`.