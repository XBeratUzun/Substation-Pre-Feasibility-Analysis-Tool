# Basic Substation Site Pre-Feasibility Checker

This is a beginner-level GIS-based web application developed using Python and Flask.  
It allows users to upload a CSV file with site coordinates and evaluates basic pre-feasibility for substation site selection.

## Features
- Reads user-uploaded site coordinates (latitude, longitude).
- Uses a simple DEM file to extract elevation using Rasterio.
- Calculates a dummy slope using Scipy.
- Performs a basic suitability check:
  - Elevation must be between 100 and 500 meters.
  - Slope must be less than 100.
- Calculates a simple estimated cost using elevation.
- Displays the results in a table on the web page.