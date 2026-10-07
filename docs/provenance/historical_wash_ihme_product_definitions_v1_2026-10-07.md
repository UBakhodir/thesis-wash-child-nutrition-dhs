# IHME W_IMP / S_IMP product definitions, resolved (2026-10-07)

Source: Local Burden of Disease WaSH Collaborators, "Mapping geographical inequalities in access to drinking water and sanitation facilities in low-income and middle-income countries, 2000–17," *Lancet Global Health* 2020 (DOI 10.1016/S2214-109X(20)30278-3), read via PMC (PMC7443708). This closes unresolved issue #4 from `historical_wash_preliminary_estimation_methods_2026-10-06.md` §9 ("Water product definition (W_IMP) and scale: unverified").

## 1. Definitions

- **Improved drinking water (W_IMP)**: piped water (on- or off-premises) **plus** "other improved" sources — protected wells and springs, bottled water, rainwater collection, bought water. These are standardised JMP (WHO/UNICEF Joint Monitoring Programme) categories, stated explicitly by the authors as aligned with JMP definitions.
- **Improved sanitation (S_IMP)**: sewer or septic sanitation **plus** "other improved" — improved latrines, ventilated improved latrines, composting toilets. Also JMP-aligned.

Both are therefore the standard, internationally recognised "at least basic" improved-facility categories, not a study-specific or ambiguous construct. The codebook's blank label for the water metric (noted in the prior methods note) is now resolved by this primary-source definition; the "W_IMP" and "S_IMP" product codes can be reported as **percent of the population with access to an improved facility, in the JMP sense**, for each raster cell.

## 2. Units, denominator, population weighting

Values are **percent of population with access** (0–100), consistent with the 0–100 scale already observed in the raster files. The paper's own reported national trend ("access to piped water increased from 40.0% to 50.3%") confirms the percentage-of-population interpretation. Estimates are population-weighted when aggregated from the continuous ~5×5 km surface to administrative units; the raw pixel-level surface used in this thesis's spatial extraction is the continuous geospatial layer itself, not a population-weighted administrative aggregate, so the extracted buffer means in this project are **area averages over the pixels inside each child's displacement buffer**, not population-weighted averages. This was already the project's working interpretation (methods note: "no percentage-of-population interpretation is asserted" beyond the 0–100 scale); it can now be stated more precisely: the scale is percent of the *local, modelled* population with access, but the extraction method used here averages pixel values by area within a buffer, not by the population each pixel represents. This distinction should be stated wherever the historical coefficients are reported (see the final reporting map).

## 3. Spatial and temporal scope

Approximately 5×5 km continuous surfaces, available 2000–2017, across low- and middle-income countries including all four study countries. Matches what the project's spatial extraction already assumed (`historical_wash_spatial_extraction_2026-10-06.md`).

## 4. Use and redistribution conditions

IHME's data-download terms (`healthdata.org` Terms and Conditions, searched directly because the GHDx record page itself returned HTTP 403 in this and the prior session) state that data made available for download is licensed for non-commercial use under the **IHME Free-of-Charge Non-Commercial User Agreement**; visualisations/graphics are separately licensed CC BY-NC-ND 4.0. A master's thesis is non-commercial academic use, consistent with permitted use under this agreement. Commercial use requires separately contacting IHME. This project's use (downloading the gridded estimates, extracting values around DHS cluster locations, and reporting aggregate statistics and regression coefficients in an academic thesis) is consistent with the non-commercial agreement as described; the full agreement text itself was not read in this pass (the GHDx page hosting it returned 403), so the thesis should cite the dataset and this source, and the author should read the complete agreement text directly from the IHME data-download page before final submission to confirm no additional condition applies.

## 5. What remains open

- The full text of the Free-of-Charge Non-Commercial User Agreement was not read (site blocked automated access); only its existence and general non-commercial scope were confirmed via search. **Action for the author**: visit the GHDx record page directly in a browser, accept the agreement as presented during download (already implicitly done when the raster files were obtained), and note the acceptance date for the data-provenance record.
- The population-weighting distinction in §2 (area-average extraction vs. the paper's population-weighted administrative aggregates) should be added as an explicit caveat in any manuscript text describing the historical coefficients.
