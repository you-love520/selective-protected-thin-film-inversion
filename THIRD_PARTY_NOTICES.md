# Third-Party Notices

This repository contains original software released under the MIT License,
together with selected third-party optical-property data and published
dispersion parameters used by the numerical models.

The MIT License in this repository applies to the original source code and
documentation authored for this project. Third-party data, published
coefficients, references, names, and associated rights remain subject to
their respective source terms and are not relicensed under the MIT License.

## 1. Silicon optical constants

Repository file:

`data/optical_constants/kla_si_optical_constants.csv`

Source:

KLA / Filmetrics Refractive Index Database, "Si, Silicon".

The KLA source page identifies the tab-delimited optical-constant data file
as available for unrestricted use. The source record cites:

Edward D. Palik, *Handbook of Optical Constants of Solids*,
Academic Press, 1985.

The data are included here only for scientific reproduction of the optical
forward model. KLA, Filmetrics, Palik, and their associated names and
trademarks are not affiliated with or endorsing this repository.

## 2. SiO2 optical constants

Repository file:

`data/optical_constants/kla_sio2_optical_constants.csv`

Source:

KLA / Filmetrics Refractive Index Database,
"SiO2, Fused Silica, Silica, Silicon Dioxide".

The KLA source page identifies the tab-delimited optical-constant data file
as available for unrestricted use. The associated refractive-index reference is:

I. H. Malitson,
"Interspecimen Comparison of the Refractive Index of Fused Silica,"
Journal of the Optical Society of America, 55, 1205–1209 (1965).

The data are included here only for scientific reproduction of the optical
forward model.

## 3. SiO2 buffer-layer and soda-lime-glass optical data

Repository files:

`data/optical_constants/zenodo_sio2_buffer_nk.csv`

`data/optical_constants/zenodo_soda_lime_nk.csv`

These files are normalized numerical representations derived from the
published optical-property dataset:

Institute of Solid State Physics, UL; Aulika, I.; Paulsone, P.;
Butikova, J.; Vembris, A.

"ITO, soda lime float glass and SiO2 buffer layer optical properties."

Zenodo dataset, DOI: 10.5281/zenodo.15055400.

Related publication:

I. Aulika, P. Paulsone, E. Laizāne, J. Butikova, and A. Vembris,
"Spatial Mapping of Optical Constants and Thickness Variations in ITO Films
and SiO2 Buffer Layers,"
Optical Materials: X, 26, 100408 (2025).

Use and redistribution of the underlying dataset remain subject to the
rights and license stated by the original Zenodo record. The normalized
files in this repository are provided solely to reproduce the numerical
optical models used in the associated study.

## 4. Analytic dispersion coefficients

The fused-silica Sellmeier coefficients implemented in
`src/stage33_anchor/optics.py` follow the published Malitson dispersion
relation cited above.

The N-BK7 Sellmeier coefficients implemented in the same source module are
based on published SCHOTT N-BK7 optical-glass dispersion data.

These published physical constants and source references remain attributed
to their original sources.

## Disclaimer

Third-party product names, organization names, trademarks, datasets, and
published parameters are acknowledged for identification and scientific
reproducibility only.

No endorsement by KLA Corporation, Filmetrics, SCHOTT, Zenodo, the
University of Latvia, or the cited authors is implied.