# Power BI Visual Specification

## Design direction

The report uses a human-centered explanatory style inspired by Alberto Cairo's
principles of clarity, honesty, context, and visible uncertainty. It does not
copy a specific Cairo work. The visual language is deliberately calm:

- warm-white canvas and Segoe UI typography;
- deep navy `#17365D` for the primary estimate;
- muted gold `#B8860B` for physical-health context;
- light navy `#5B7FA3` for the supporting mental-health panel;
- warm gray `#73777A` for secondary copy;
- direct labels, fixed zero baselines, and no decorative icons or gradients.

Groups are shown in the fixed analytical order Christian, Other faith, and No
religious affiliation. Color is not used to imply that one group is better or
worse than another.

## Page 1 — Mental Health

- Canvas: 1600 × 1080; first and active page.
- Title: **Frequent mentally unhealthy days differ across religious-affiliation groups**
- Subtitle: **Share of U.S. adults reporting 8+ mentally unhealthy days in the past month, GSS 2022**
- Release target: a horizontal dot-and-whisker display, with the dot marking
  the estimate and a line marking its asymmetric 95% confidence interval.
- Current Desktop prototype: a native horizontal bar chart with absolute,
  field-driven confidence bounds. A model-driven SVG dot-and-whisker measure is
  under review as a dependency-free way to achieve the target visual form.
- Scale: fixed 0–35%.
- Values: 14.65%, 22.52%, and 25.42%.
- Tooltip: lower bound, upper bound, and valid respondent count.
- Sample context is repeated below the chart so it remains available in static
  exports.

## Page 2 — Full Health Overview

- Canvas: 1600 × 1080, matching the Python reference composition.
- Top: excellent or good general health on a fixed 0–100% scale.
- Bottom left: 8+ physically unhealthy days on a fixed 0–35% scale.
- Bottom right: 8+ mentally unhealthy days on the same fixed 0–35% scale.
- All three native visuals use absolute, field-driven 95% confidence intervals,
  direct labels, fixed group order, contextual sample sizes, and accessible alt
  text.
- Physical and mental health use both different titles and different colors;
  interpretation never depends on color alone.

## Model and provenance

The PBIP project is in `powerbi/project/ChristianWellbeing2022/`. Its
`ChartData` table embeds only the nine reviewed aggregate rows from
`data/processed/chart_data.csv`; it contains no respondent-level records and no
absolute local paths. Required measures are `Estimate %`, `CI Low %`,
`CI High %`, `Valid Respondents`, and `Source Label`, plus metric-specific
measures used to keep each visual filter-safe.

Source: General Social Survey 2022. Estimates use `WTSSNRPS`; 95% confidence
intervals use the survey design variables `VSTRAT` and `VPSU`.

## Interpretation and accessibility

The report keeps this qualification adjacent to the evidence:

> These are descriptive differences, not evidence that faith causes better or worse health.

No religious affiliation is not equivalent to atheist. Samples differ by
metric. Every chart includes alt text, direct values, sample context, and
confidence intervals. Related panels use compatible scales and remain readable
without a legend.

## QA checklist

- Open the `.pbip` file in Power BI Desktop and refresh the embedded table.
- Confirm both pages load without repair or schema warnings.
- Confirm all nine estimates, intervals, and sample sizes match the CSV.
- Confirm Mental Health opens first and the group order is stable.
- Confirm error bars are asymmetric and use absolute bounds.
- Exercise tooltips and verify the fixed axes (0–35%, 0–100%).
- Inspect exported pages for clipping, overlap, grayscale legibility, and source
  visibility.
- Run `python -m unittest discover -s tests -v` and
  `Invoke-PowerBIUnifiedReview.ps1 -SkipLive` before release.
