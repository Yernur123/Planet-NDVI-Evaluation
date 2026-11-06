# Agricultural Monitoring Prototype - PlanetScope NDVI
## 1. Project overview
This prototype explores how optical satellite imagery can support field-level agricultural monitoring. It compares vegetation development across three selected agricultural fields in Brandenburg, Germany, using PlanetScope NDVI observations exported from the Planet Sandbox Analysis-Ready PlanetScope NDVI workflow.

The prototype is intended for exploratory monitoring. It helps a user compare vegetation trends, identify observations that deserve closer inspection, and review available data-quality indicators. It does not classify crops, estimate yield, or determine the cause of a vegetation change.

## 2. Objective and analytical questions
The prototype addresses the following questions:
- How does vegetation development differ across the three selected fields during the 2023 growing season?
- When does each field reach its highest observed mean NDVI?
- Are there unusually large changes between consecutive observations?
- Do available quality indicators (such as cloud coverage, sample count, and no-data count) help explain or qualify those observations?

## 3. Data
- Platform/workflow: Planet Sandbox, Analysis-Ready PlanetScope NDVI.
- Area of interest: selected agricultural fields in Brandenburg,
Germany.
- Analysis period requested: 1 April--31 October 2023.
- Unit of analysis: one field and one observation date.
- Input: field-level CSV statistics exported from the Planet workflow and combined into "Analysis_PlanetScope_Sandbox_All - All data.csv"

### Relevant attributes
The exported files include field/date identifiers and NDVI summary
statistics. Depending on the exported schema, the dataset may include:
- date: observation date.
- field_id: identifier assigned to the selected field.
- mean, median, min, max: field-level NDVI statistics.
- stdev, p10, p90: distribution statistics, where present.
- samplecount, nodatacount: pixel/sample counts, where present.
- cloudcoveragepercent: cloud-coverage indicator, where present.
The exact column names in the exported CSV should be retained. Some Planet-exported statistic columns may have a long collection/product prefix.

### Data provenance note: the values analysed here are Planet-exported
NDVI statistics. This prototype does not claim to independently calculate NDVI from raw red and near-infrared bands.

## 4. Preparation and processing
1. Export field-level NDVI statistics for each selected field from the Planet workflow.
2. Combine the three field exports into one table, adding or retaining a field_id to distinguish the fields.
3. Parse observation dates and sort records by field and date.
4. Review missing values and the availability of quality-related columns.
5. Calculate the change in mean NDVI between consecutive observations for each field:
   ndvi_change = mean NDVI at current observation - mean NDVI at previous observation
   The calculation is performed separately for each field. It is a difference between consecutive records, not a rate per day; observation intervals may vary.
6. Summarise average, maximum, and minimum mean NDVI and the number of observations for each field.
7. Visualise the time series and flag large absolute changes for further inspection.
No observations should be removed solely because they look unusual.
Large changes are treated as review flags until their quality and context have been checked.

## 5. Prototype functionality
The Streamlit application (streamlit.py) provides:
- Field selection and date-range filtering.
- Overview metrics for selected fields and observations.
- An interactive NDVI time-series chart.
- A field selector with individual-field metrics.
- Tabs for the NDVI trend, NDVI distribution, and available quality attributes.
- A configurable threshold to flag large consecutive-observation NDVI changes.
- CSV export of the filtered observations.
The dashboard is an exploratory interface. A flagged observation is not automatically an agricultural event.

## 6. Initial observations 
The current analysis produced the following field-level summary:
Field   | Average mean NDVI | Maximum mean NDVI | Minimum mean NDVI | Observations
Field_1       0.541037        0.708809              0.111914                  103
Field_2       0.591447        0.750918              0.133420                  100
Field_3       0.619292        0.789504              0.112364                  101

Observed peak dates:
- Field 1: 3 July 2023 (mean NDVI 0.709).
- Field 2: 13 August 2023 (mean NDVI 0.751).
- Field 3: 14 August 2023 (mean NDVI 0.790).

### Interpretation
- Field 3 had the highest average and maximum mean NDVI among the three fields in this dataset.
- Field 1 reached its maximum earlier than Fields 2 and 3.
- Field 3 showed several unusually large changes between consecutive observations, including sharp decreases and increases in July and August.
- These differences are useful signals for investigation, but they do not establish why vegetation conditions changed.
The unusually large Field 3 changes should be reviewed against cloud coverage, sample count, no-data count, acquisition dates, and the underlying imagery before drawing an agricultural conclusion. The same quality review should be applied consistently to all fields.

## 7. Limitations and assumptions
- NDVI is an indicator of vegetation greenness/activity, not a direct measurement of crop health, biomass, or yield.
- NDVI changes can be associated with real field changes, but can also be affected by clouds, haze, shadows, atmospheric conditions, image processing, valid-pixel coverage, and differences between observation dates.
- A difference between consecutive observations does not account for the number of days between them.
- The three selected fields are a small exploratory sample and should not be treated as representative of the wider region.
- Field-level averages can hide within-field variation. Spatial inspection of the imagery and field boundaries would be needed to investigate localised patterns.
- The prototype does not identify crop type or distinguish planting, harvesting, irrigation, disease, or other causes.
- Any missing or unreliable observations should be documented rather than silently interpreted as stable vegetation.

## 8. How to run the application
### Requirements
- Python 3.10 or a compatible Python version.
- The packages used by the application: streamlit, pandas, and plotly.
- app.py and merged_ndvi.csv in the same project directory, unless the CSV path in the application is adjusted.
### Setup
Create and activate a virtual environment if one is not already available:
``` python -m venv .venv
source .venv/bin/activate
```
Install the dependencies:
```
python -m pip install streamlit pandas plotly
```
Run the application from the project directory:
```
streamlit run streamlit.py
````
Open the local URL printed in the terminal (http://localhost:####).

## 9. Use of AI assistance
AI assistance was used to support coding, debugging, dashboard structuring, and documentation. The data source and analytical results are based on the Planet-exported field-level NDVI statistics. All interpretations remain subject to validation against imagery and relevant field context.
