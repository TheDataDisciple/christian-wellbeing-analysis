# Power BI Visual Specification

## Design direction

The two-page editorial report uses a human-centered explanatory style inspired
by Alberto Cairo's principles of clarity, honesty, context, and uncertainty.
It does not reproduce a particular Cairo design. Georgia headings, navy bars,
direct percentage labels, quiet respondent notes, and generous whitespace keep
attention on the comparison. Numeric axes, gridlines, decorative marks, and
visible error bars are suppressed in the current design.

The order is always Christian, Other faith, and No religious affiliation.
Color does not encode spiritual worth or a causal claim. The bars have zero
baselines and fixed metric-appropriate ranges. The 95% confidence intervals
remain bound to data fields and are available in interactive tooltips, not in
static screenshots.

## Page 1 — 01 | Mental Health

- Canvas: 1600 × 1080; opening page.
- One native horizontal bar chart: share of U.S. adults reporting 8+ mentally
  unhealthy days in the past month, GSS 2022.
- Estimates: Christian 14.65%; Other faith 22.52%; No religious affiliation
  25.42%.
- Fixed scale: 0–35%. The chart displays direct percentages and a note with
  valid respondent counts of 1,157, 125, and 591 respectively.
- Tooltip fields: estimate, lower and upper 95% confidence bounds, and valid
  respondent count.

## Page 2 — 02 | Health Context

- Canvas: 1600 × 1080, matching the opening page's editorial treatment.
- Top native horizontal bar chart: excellent or good general health, fixed
  0–100% scale; estimates 72.45%, 75.85%, and 70.96%.
- Bottom native horizontal bar chart: 8+ physically unhealthy days in the
  past month, fixed 0–35% scale; estimates 8.48%, 8.83%, and 11.10%.
- Each chart has direct percentages, a metric-specific respondent note,
  accessible alt text, and tooltip-bound 95% confidence limits.

## Model and provenance

The text-based PBIP project is in `powerbi/project/ChristianWellbeing2022/`.
Its Power Query M `ChartData` partition embeds only the nine reviewed
aggregate rows from `data/processed/chart_data.csv`; it contains no
respondent-level records or absolute local paths. TMDL defines the semantic
model and DAX measures. PBIR files define the pages and visuals.

Source: General Social Survey 2022. Estimates use `WTSSNRPS`; 95% confidence
intervals use the survey-design variables `VSTRAT` and `VPSU`. Metric-specific
missing responses are excluded; valid sample sizes therefore differ.

## Interpretation and accessibility

These are descriptive differences, not evidence that faith causes better or
worse health. No religious affiliation is not equivalent to atheist. The Other
faith group is smaller and has wider confidence intervals. The report and its
accompanying copy should make those caveats visible even though the intervals
themselves appear only on hover. All three charts have direct values and alt
text; interpretation does not depend on color alone.

## Release checks

- Open the `.pbip` in Power BI Desktop and confirm both pages load without
  repair or schema warnings, with Mental Health first.
- Compare all nine estimates, interval bounds, and respondent counts with the
  processed CSV; exercise tooltips on all three charts.
- Verify fixed zero-based scales, group order, visible source/caveat copy, and
  alt text in Desktop and in Power BI Service.
- Export both pages and inspect for clipping, overlap, and readability before
  making a Desktop screenshot the README lead image.
- Run `python -m unittest discover -s tests -v` and the offline Power BI review
  before marking the PR ready.
