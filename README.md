# Basic Substation Site Pre-Feasibility Checker

This is a beginner-level GIS-based web application developed using Python.  
The app allows users to **upload only a DEM file (`.tif`)**, and it automatically analyzes the terrain and generates a basic **Bill of Materials (BoM)** estimation for substation site pre-feasibility.

## Features
- Upload **only a DEM (`.tif`) file**.
- Reads and analyzes the **elevation data from the DEM**.
- Calculates:
  - Mean, Min, Max elevation.
  - Approximate average slope using a simple Sobel filter.
  - Total area within **100-500 meters elevation range**.
- Automatically estimates a basic **Bill of Materials (BoM)**:
  - Excavation volume (based on area and depth).
  - Concrete and steel quantity estimates.
  - **Estimated cost.**
- Presents results and BoM in a **simple web page table**.
