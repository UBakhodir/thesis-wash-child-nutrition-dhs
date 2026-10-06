# Historical WASH: spatial extraction of IHME modelled WASH coverage (2026-10-06)

Status: method, validation and coverage record. Cluster-level extracted values and coordinates are restricted and are not published here. The extraction is a technical operation on IHME modelled surfaces. No outcome analysis, no child exposure window and no regression have been run, and nothing here is a thesis result.

## 1. Authorization (round-level, supersedes earlier status)

- The DHS Program dataset account for the thesis project shows GPS download access for each of the four rounds used: Ethiopia 2016, Ghana 2014, Kenya 2014 and Nigeria 2018. It also shows SURVEY and GPS approval for all four countries.
- Access is confirmed for download, not for redistribution. The DHS GPS data-use conditions were not verified here. Coordinate-derived records are kept outside the repository.
- Phase labels on the account pages are DHS-7 for all four rounds. This conflicts with the IPUMS explanation that KIDCURAGEMO is "Phase VII forward" (it is blank for Ghana 2014 and Kenya 2014 in the extract). The cause of the blank values is unresolved and is included in the open support question.

## 2. Coordinate-to-survey correspondence (verified, aggregate)

- DHSID structure (country code, survey year, cluster number) matches each sample for all rows.
- Each PSU maps to one DHSID and each DHSID to one PSU.
- All usable coordinates fall inside approximate national boxes (sanity check only).
- Usable clusters: 4,011 (Ethiopia 622; Ghana 423; Kenya 1,584; Nigeria 1,382). Clusters with conflicting coordinates or classification: none excluded.

## 3. Projection and buffer method

- Raster: IHME grid, EPSG:4326 (checked from the GeoTIFF GeoKey), raster type PixelIsArea, pixel 0.041667 degrees, shape 2,123 by 6,610, NoData -999999, valid values 0–100.
- Coordinate order: GPSLAT is latitude, GPSLONG is longitude (WGS84). Raster x is longitude, y is latitude.
- Projection: an azimuthal equidistant projection (AEQD) centred on each cluster. Distance from the cluster centre is exact by construction. A self-test compared AEQD radial distances with geodesic distances: maximum relative error 6 × 10⁻¹² over 200 random pairs.
- Equal-area alternative rejected: ESRI:102022 (Africa Albers) has a meridional-to-parallel scale difference of up to about 15% over the study area, so circular buffers would be distorted.
- Buffers: urban 2 km; rural 5 km (primary); rural 10 km (sensitivity, for the 1% of rural clusters displaced up to 10 km). Displacement rule from IPUMS (GPSLAT documentation): urban up to 2 km; 99% of rural up to 5 km; 1% of rural up to 10 km.
- Averaging: area-weighted. Each IHME pixel is represented by its projected quadrilateral, and its exact overlap with the disk is computed (circle–triangle decomposition). The geographic mean is the area-weighted mean over covered buffer area. This is a geographic area average, not a population-weighted coverage estimate.
- Partial coverage is never renormalised to full coverage. Each buffer records total area, valid area, valid-area fraction, number of contributing cells, and the outside-raster and NoData fractions.
- Numerical tolerance for full coverage: 1 × 10⁻³ of buffer area.
- Point method (sensitivity): containing-pixel rule only. If the containing cell is NoData, the result is missing; no nearest valid cell is substituted.
- Refugee-coded clusters (URBAN = 3): none are present among the usable clusters in this extract.

## 4. Tests and checks

Self-test against analytic values and independent Monte Carlo references (random points uniform in the disk, mapped back to lon/lat), on synthetic rasters:

| Check | Result |
|---|---|
| Constant raster: buffer mean returns the constant, full coverage | pass |
| Total buffer area equals pi R² (R = 1, 2, 5, 10 km), within 0.01% | pass (all four) |
| Small buffer smaller than one cell: few contributing cells | pass |
| Fractional overlap: mean and valid fraction vs Monte Carlo | pass |
| NoData: mean is the valid value only; never zero; partial status | pass |
| All-NoData buffer: missing, not zero | pass |
| Buffer crossing cell boundaries (two-valued raster) vs Monte Carlo | pass |
| Raster edge: valid fraction vs Monte Carlo; partial status | pass |
| AEQD radial distance vs geodesic distance | pass |

Earlier version 09 (sub-sampled overlap) FAILED its self-test: its area error at 1–2 km buffers was large and did not converge with finer sampling. It was kept as a record and not used for any output. Version 10 replaced it with exact overlap.

Pilot on 20 real clusters (fixed random seed) against Monte Carlo on one real raster (Water MEAN, 2016), aggregate only:
- median absolute difference in mean: 0.010 percentage points;
- maximum absolute difference in mean: 0.12 percentage points (Monte Carlo sampling noise on heterogeneous cells);
- maximum absolute difference in valid-area fraction: 0.0008.

## 5. Products, inputs and overlap

- Archive members: S_IMP (sanitation) and W_IMP (water), each with LOWER, MEAN and UPPER estimates for 2000–2017. All 54 members per product are present, with the expected names.
- IHME codebook: the metric for S_IMP is "Percent". The metric for W_IMP is blank in the codebook. The units used here are taken from the file names and the 0–100 range; the W_IMP metric is unverified.
- The codebook labels LOWER and UPPER as "Lower / Upper Confidence Interval". The confidence level is not stated in the codebook, so none is assumed. Extracted LOWER and UPPER values are spatial averages of the supplied bounds, not uncertainty intervals for the buffer mean.
- Overlap with DHS inputs (IHME input-source workbooks, 2014–2018 entries): Ghana 2014 is a DHS input for both products. Kenya 2014 is a DHS input for water only. Ethiopia's DHS input is the 2014 survey (not 2016). Nigeria 2018 and Ethiopia 2016 are not DHS inputs for either product in these workbooks. Ethiopia 2016 sanitation has a country-specific input source. The overlap means some extracted values for Ghana and Kenya are model estimates that use the same survey family; this is documented, not corrected.

## 6. Execution and validation (aggregate)

Run: restricted outputs in a local run folder outside the repository (run identifier recorded in the local manifest).

| Item | Result |
|---|---|
| Rows | 1,126,440 |
| Primary buffers (urban 2 km, rural 5 km) | 4,011 clusters × 2 products × 3 estimates × 18 years |
| Rural 10 km sensitivity | 2,408 clusters |
| Containing-pixel sensitivity | 4,011 clusters |
| Years | 2000–2017, complete |
| Duplicate keys | 0 |
| Cluster-method groups with the expected 108 rows | all (10,430 of 10,430) |
| Covered values not finite | 0 |
| Covered values outside 0–100 | 0 |
| Missing rows carrying a value | 0 |
| LOWER ≤ MEAN ≤ UPPER violations | 0 of 374,040 comparable triples |

Coverage, primary buffers (per product; both products are identical in coverage):

| Status | Rows |
|---|---|
| Full | 209,520 |
| Partial (valid fraction kept; not renormalised) | 6,804 |
| Missing (all NoData) | 270 |

Coverage, sensitivity methods:
- Rural 10 km: full 121,500; partial 8,424; missing 108 (per product).
- Containing pixel: full 214,812; missing 1,782 (per product); no partial values by definition.

Missingness reasons: partial buffers are all NoData-driven (no buffer had any area outside the raster grid; the grid extends beyond all cluster surroundings). Median NoData share of partial primary buffers is about 15%. The cause of NoData inside the grid is not documented here and is recorded as unresolved (plausibly water bodies and other unmodelled areas; not verified).

Buffer minus point (MEAN, both defined; 143,208 pairs): median difference 0.0 for both products; 5th–95th percentile about −13 to +13 points for sanitation and −18 to +18 for water. These large differences show that point and buffer extraction answer different questions when cells are heterogeneous. Neither method was selected on the basis of any outcome.

## 7. Remaining limitations

- Spatial assignment: displacement means the true location is not recovered by any buffer. The buffers address spatial-assignment uncertainty; they are not a validated probability distribution of displacement.
- Current residence is a proxy for historical residence; migration is not observed.
- IHME values are modelled estimates. The LOWER/UPPER bounds are not uncertainty intervals for buffer means.
- Overlap with DHS inputs (section 5).
- Product definitions for W_IMP metric and the NoData cause remain unresolved.
- Ethiopia: extraction does not depend on its interview calendar; the Ethiopian interview-date conversion remains provisional and is not used here.

## 8. Next step

Child exposure-window construction, in a separate milestone. Before it: settle which Gregorian interview timing is used for Ethiopia (still provisional), confirm the KIDCURAGEMO support question, and confirm the measurement-subsample weighting approach.
