# Addendum: geometry and denominator wording for the spatial extraction (2026-10-06)

This addendum corrects and clarifies the wording in historical_wash_spatial_extraction_2026-10-06.md. The earlier document is not edited; this addendum supersedes its geometry wording.

## 1. Correction of "exact" wording

The earlier document described the overlap as "exact polygon-disk overlap". That is accurate only for the disk. The precise description is:

- The disk boundary is exact: the overlap of each pixel with the disk is computed analytically (circle–triangle decomposition).
- Each pixel is represented by a quadrilateral whose four corners are the projected pixel corners in the cluster-centred azimuthal equidistant projection. Its edges are straight corner-to-corner segments, not densified.

So the overlap is exact with respect to a straight-edged pixel model. The pixel edges (lines of constant latitude or longitude) are curves in the projection; the straight-edge model approximates them.

## 2. Evidence that the approximation is small for these buffers

On 150 real clusters, each buffer compared with a model whose pixel edges are densified (16 points per edge, sampled in longitude and latitude before projection):

| Quantity | Result |
|---|---|
| Per-pixel area, relative difference (median / 99th percentile / maximum) | 1.6 × 10⁻⁸ / 2.1 × 10⁻⁸ / 2.1 × 10⁻⁸ |
| Buffer mean, absolute difference in IHME percent (median / maximum) | 0.00002 / 0.001 |
| Valid-area fraction, absolute difference (maximum) | 7 × 10⁻⁷ |

Total buffer area agrees with π R² to machine precision for both edge models. This agreement is a property of the tiling (adjacent pixels share corners), not evidence about the edge approximation, and it is not used as such.

Conclusion: at the buffer scales used (2, 5 and 10 km) and pixel size (about 4.6 km), the straight-edge approximation changes buffer means by negligible amounts. The approximation is therefore adequate for this use.

## 3. Denominator of the spatial mean (confirmed)

For a buffer with partial coverage, the reported mean is

    mean = Σ_k (value_k × valid overlap area_k) ÷ Σ_k (valid overlap area_k),

where the sums run over pixels inside the raster, with a value that is not NoData and lies in 0–100.

- Missing raster area (outside the raster or NoData) adds to neither the numerator nor the denominator. It is never treated as zero.
- The total buffer area is used only to compute the valid-area fraction, which is reported separately. A partial-buffer mean is not described as complete coverage.
- On the test clusters, using total buffer area as the denominator (with NoData treated as zero) would change partial-buffer means by up to 73 percentage points (median 0.9). The implemented formula is the required one; no correction and no rerun of the extraction were needed.

## 4. Consequence for the existing extraction

The extraction run (run_v3_20261006T183003Z) is unchanged and remains valid. This addendum changes wording only; the numerical outputs are unaffected.
