# Source-Code Notes

The source tree is normalized for the Stage33 / Final A+B public package.

- `stage33_anchor/` contains the robust-anchor and forward-model modules inherited from the implementation line.
- `final_ab/` contains the adaptive physics-protected refinement and selective-routing implementation.

The public manuscript result identity is fixed by `configs/final_ab_parameters.json`, `configs/protected_refinement_parameters.json`, and the manuscript-aligned summary tables. Public summary verification and result-building entry points are placed in `analysis/`; they do not run the estimator.

The fixed-result verifier is `analysis/verify_stage33_release.py`.
