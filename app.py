from flask import Flask, render_template, request
import rasterio
from scipy import ndimage
import numpy as np

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_dem():
    file = request.files['file']
    
    # Save uploaded DEM temporarily
    dem_path = 'uploaded_dem.tif'
    file.save(dem_path)
    
    # Open DEM
    dem = rasterio.open(dem_path)
    elevation_data = dem.read(1)
    
    # Mask no data values
    elevation_data = np.where(elevation_data == dem.nodata, np.nan, elevation_data)
    
    # Elevation stats
    mean_elev = np.nanmean(elevation_data)
    min_elev = np.nanmin(elevation_data)
    max_elev = np.nanmax(elevation_data)
    
    # Slope calculation
    dx = ndimage.sobel(elevation_data, axis=0, mode='constant', cval=np.nan)
    dy = ndimage.sobel(elevation_data, axis=1, mode='constant', cval=np.nan)
    slope = np.hypot(dx, dy)
    mean_slope = np.nanmean(slope)
    
    # Calculate area where elevation is between 100 and 500 meters
    suitable_mask = (elevation_data >= 100) & (elevation_data <= 500)
    suitable_cells = np.count_nonzero(suitable_mask)
    pixel_area = dem.res[0] * dem.res[1]
    total_area_m2 = suitable_cells * pixel_area * (111320 ** 2)

    # BoM estimates
    excavation_volume = total_area_m2 * 2
    concrete_tons = excavation_volume * 0.1
    steel_tons = excavation_volume * 0.02
    estimated_cost = excavation_volume * 5

    # Create HTML output
    result = f"""
    <h2>DEM Analysis Results</h2>
    <ul>
        <li>Mean Elevation: {mean_elev:.2f} meters</li>
        <li>Min Elevation: {min_elev:.2f} meters</li>
        <li>Max Elevation: {max_elev:.2f} meters</li>
        <li>Average Slope (approximate): {mean_slope:.2f}</li>
        <li>Total Suitable Area (approx): {total_area_m2/1e6:.2f} km²</li>
    </ul>
    <h2>Estimated BoM (Bill of Materials)</h2>
    <table border="1">
        <tr><th>Item</th><th>Quantity</th></tr>
        <tr><td>Excavation Volume</td><td>{excavation_volume:.2f} m³</td></tr>
        <tr><td>Concrete</td><td>{concrete_tons:.2f} tons</td></tr>
        <tr><td>Steel</td><td>{steel_tons:.2f} tons</td></tr>
        <tr><td>Estimated Cost</td><td>${estimated_cost:,.2f}</td></tr>
    </table>
    """
    return result

if __name__ == '__main__':
    app.run(debug=True)
