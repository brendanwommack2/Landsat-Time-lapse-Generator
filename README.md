**Surface Change Analysis and Timelapse Generation with Landsat 8**

_**Overview**_

This project uses the Google Earth Engine (GEE) Python API to create time-series analyses and timelapse videos from Landsat 8 imagery. The script processes imagery for predefined regions, applies cloud filtering, computes key spectral indices, and exports both visualizations and quantitative metrics to Google Drive.
The workflow demonstrates how satellite data can be used to monitor environmental change and support resource management decisions in areas affected by drought, urban expansion, or ecosystem stress.

_**Key Features**_

  Automated retrieval of Landsat 8 imagery by path/row and date range
  Cloud masking and spectral index computation for NDVI, NDWI, and NDBI
  Export of timelapse videos (RGB composites) to Google Drive
  Export of surface change metrics (vegetation, water, urban area) as CSV
  Configurable region scope

_**Methods**_
1. Data Filtering
  Landsat 8 Collection 2 Level-1 TOA imagery
  Cloud cover <5%
  Optional start and end dates
2. Index Calculation
  NDVI (B5, B4): vegetation health
  NDWI (B3, B5): surface water
  NDBI (B6, B5): built-up areas
3. Area Summaries
  Compute total vegetation, water, and urban area in m²
  Derive mean NDVI for each date
4. Export
  CSV of time-series metrics (*_surface_change_metrics.csv)
  Video timelapse of RGB composites (*_timelapse_video.mp4)

Example Region: Lake Mead
The accompanying Jupyter Notebook visualizes trends in vegetation (NDVI) and water extent (NDWI) for the Lake Mead watershed.
The results show a decline in vegetation and surface water area since 2013, consistent with ongoing drought and reduced inflows.

_**Tools and Libraries**_

  Google Earth Engine (Python API)
  pandas, numpy, matplotlib
  Anaconda Python 3.10+

_**Usage**_

python BuildTimelapse_Analysis.py <region> [start_date end_date]

Example:
python BuildTimelapse_Analysis.py lakemead 2013-01-01 2024-12-31

Exports will appear in your linked Google Drive account under the specified region.

_**Key Skills Demonstrated**_

Remote sensing and geospatial analysis using GEE
Python scripting and data automation
Satellite-based environmental monitoring
Quantitative analysis and visualization of surface change

_**Author**_

Brendan Wommack
M.S. Geospatial Data Sciences | University of Michigan
Geospatial Specialist | Virginia Institute of Marine Science
joelbrendanwommack.com
