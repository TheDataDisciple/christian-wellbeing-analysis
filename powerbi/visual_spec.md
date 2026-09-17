# Power BI Visual Specification

## Page

- Name: **Faith and Health**
- Canvas: 16:9, white background
- Header: **Faith and self-reported health in the United States**
- Subtitle: **Survey-weighted descriptive estimates, GSS 2022**
- Qualification: **Association does not establish that faith causes health outcomes.**

## Service implementation

The Power BI Service report uses a single clustered horizontal bar chart with
all three metrics, a zero baseline, direct value labels, and a visible
"descriptive association, not causation" subtitle. This layout keeps the
aggregate-only web report legible in one view. The reproducible PNG/PDF export
implements the two-panel design below and displays the 95% confidence intervals
directly.

## Main visual

- Native clustered horizontal bar chart
- Filter: `metric_id = good_or_better_pct`
- Y-axis: `belief_group`, sorted by `sort_order`
- X-axis: `Estimate %`, fixed from 0% to 100%
- Error bars: lower `CI Low %`, upper `CI High %`
- Direct labels: one decimal place
- Tooltip: metric label, estimate, confidence bounds, valid respondents
- Color: single deep navy (`#17324D`); identity is already carried by the axis
- Title: **Most adults in every affiliation group report good or excellent health**

## Supporting visual

- Native clustered horizontal bar chart
- Filter: `metric_id` in `physical_8plus_pct`, `mental_8plus_pct`
- Y-axis: `belief_group`, sorted by `sort_order`
- Series: `metric_label`
- X-axis: 0% to 35%
- Error bars use the corresponding lower and upper measures
- Colors: navy for physical health, muted gold for mental health
- Title: **Frequent mentally unhealthy days vary more than physical-health days**

## Footer

- Source label from the DAX measure
- Note: “No religious affiliation is not equivalent to atheist. Samples differ by metric.”
- Link text: “Methods and reproducible code: GitHub”

## Accessibility and QA

- Add descriptive alt text to each visual.
- Do not rely on color alone; retain direct series labels and tooltips.
- Verify every displayed number against `chart_data.csv`.
- Inspect at standard and narrow browser widths and in grayscale.
- Static exports are generated with `python scripts/render_chart.py` from
  `data/processed/chart_data.csv`.
