# Power BI Visual Specification

## Design direction

The two-page report uses a human-centered explanatory style inspired by
Alberto Cairo's principles of clarity, honesty, context, and uncertainty. It
does not reproduce a particular Cairo design. Georgia headings, navy bars,
direct percentage labels, quiet respondent notes, and generous whitespace keep
attention on the comparison.

The group order is always Christian, Other faith, and No religious
affiliation. Color does not encode spiritual worth or a causal claim. The bars
have zero baselines and fixed metric-appropriate ranges. Survey-design-adjusted
95% confidence intervals remain bound to data fields and appear in interactive
tooltips rather than as visible marks.

## Page 1 — 01 | Mental Health

### Desktop

- Canvas: 1600 × 1080; opening page.
- One native horizontal bar chart: share of U.S. adults reporting 8+ mentally
  unhealthy days in the past month, GSS 2022.
- Estimates: Christian 14.65%; Other faith 22.52%; No religious affiliation
  25.42%.
- Fixed scale: 0–35%, with direct percentages and valid respondent counts of
  1,157, 125, and 591.
- Tooltip fields: estimate, lower and upper 95% confidence bounds, and valid
  respondent count.

### Phone portrait

- Width: 323 Power BI mobile-layout units.
- Full-width order: `Dashboard_current`, then `Dashboard_current_note`.
- The primary comparison occupies the first screen; the respondent note
  follows with an 8-unit gap.

## Page 2 — 02 | Health Context

### Desktop

- Canvas: 1600 × 1080, matching the opening page's editorial treatment.
- Top native horizontal bar chart: excellent or good general health, fixed
  0–100% scale; estimates 72.45%, 75.85%, and 70.96%.
- Bottom native horizontal bar chart: 8+ physically unhealthy days in the
  past month, fixed 0–35% scale; estimates 8.48%, 8.83%, and 11.10%.
- Each chart has direct percentages, a metric-specific respondent note,
  accessible alt text, and tooltip-bound 95% confidence limits.

### Phone portrait

- Width: 323 Power BI mobile-layout units.
- Full-width order: `Growth_title`, `Growth_subtitle`, `Growth_current`,
  `Growth_current_note`, `Growth_gain`, and `Growth_gain_note`.
- The charts are stacked vertically and never placed side by side. Gaps are at
  least 8 units; chart heights are 300 units to avoid internal scrolling.

## Model and provenance

The text-based PBIP project is in `powerbi/project/ChristianWellbeing2022/`.
Its Power Query M `ChartData` partition embeds only the nine reviewed aggregate
rows from `data/processed/chart_data.csv`; it contains no respondent-level
records or absolute local paths. TMDL defines the semantic model and DAX
measures. PBIR files define the pages, desktop visuals, and portrait mobile
positions.

Source: General Social Survey 2022. Estimates use `WTSSNRPS`; 95% confidence
intervals use `VSTRAT` and `VPSU`. Metric-specific missing responses are
excluded, so valid sample sizes differ.

## Public delivery

The canonical anonymous report is:

https://app.powerbi.com/view?r=eyJrIjoiMWNmYzlkY2UtOGZjOS00ZTFiLWJmY2UtOTIxYTkwMDM5MGFiIiwidCI6ImEwNzg4YjhlLWYwNDktNGY1YS04OGEyLTY3NTliZWY2OWM3NiIsImMiOjl9&pageName=MentalHealthEditorial

It must open on `MentalHealthEditorial`, show two pages, and require no Power BI
sign-in. Publication must update the report behind this URL without creating or
deleting an embed code.

## Interpretation and accessibility

These are descriptive differences, not evidence that faith causes better or
worse health. No religious affiliation is not equivalent to atheist. The Other
faith group is smaller and has wider confidence intervals. All charts have
direct values and alt text, and interpretation does not depend on color alone.

## Release checks

- Open the `.pbip` in Power BI Desktop and confirm both desktop and phone
  layouts load without repair or schema warnings.
- Compare all nine estimates, interval bounds, and respondent counts with the
  processed CSV; exercise tooltips on all three charts.
- Inspect the two-page PDF and page PNGs for clipping, overlap, and readability.
- Inspect both portrait layouts for full-width order, readable labels, and no
  internal scrolling.
- Run `python -m unittest discover -s tests -v` and the offline Power BI review.
- After publication, verify both pages through the canonical anonymous URL at
  desktop and phone viewport sizes.
