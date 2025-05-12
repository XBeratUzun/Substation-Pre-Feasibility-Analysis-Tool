from flask import Flask, render_template, request
import pandas as pd
import geopandas as gpd
import rasterio
from shapely.geometry import Point
from scipy import ndimage
import numpy as np

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_file():
    # Read uploaded CSV
    file = request.files['file']
    df = pd.read_csv(file)

    # Open DEM file
    dem_file = 'data/sample_dem.tif'
    dem = rasterio.open(dem_file)

    results = []

    for _, row in df.iterrows():
        site_name = row['Site Name']
        lon = row['Longitude']
        lat = row['Latitude']

        # Get row, col from lon, lat
        row_col = dem.index(lon, lat)
        elevation = dem.read(1)[row_col[0], row_col[1]]

        # Dummy slope using simple Sobel filter
        elevation_data = dem.read(1)
        dx = ndimage.sobel(elevation_data, 0)
        dy = ndimage.sobel(elevation_data, 1)
        slope = np.hypot(dx[row_col[0], row_col[1]], dy[row_col[0], row_col[1]])

        # Create buffer using Shapely (1km buffer just as example)
        point = Point(lon, lat)
        buffer = point.buffer(0.01)  # Approx 1km

        # Dummy suitability check
        suitability = 'Suitable' if 100 < elevation < 500 and slope < 100 else 'Not Suitable'

        # Dummy cost
        cost = 10000 + elevation * 2

        results.append({
            'Site Name': site_name,
            'Elevation': elevation,
            'Slope': slope,
            'Suitability': suitability,
            'Estimated Cost': cost
        })

    # Create DataFrame for results
    results_df = pd.DataFrame(results)

    return results_df.to_html(index=False)

if __name__ == '__main__':
    app.run(debug=True)