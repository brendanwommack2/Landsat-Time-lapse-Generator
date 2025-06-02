import ee
from ee import batch
import sys

# Configure project ID
ProjectID = "buildtimelapse"

# Initialize Earth Engine
ee.Initialize(project=ProjectID)

# Define supported regions with WRS path/row and bounding box coordinates
REGIONS = {
    "dubai": {
        "path": 160,
        "row": 43,
        "region": [
            [55.6458, 25.3540],
            [54.8135, 25.3540],
            [54.8135, 24.8042],
            [55.6458, 24.8042]
        ]
    },
    "miami": {
        "path": 15,
        "row": 42,
        "region": [
            [-80.4, 25.9],
            [-80.3, 25.9],
            [-80.3, 25.6],
            [-80.4, 25.6]
        ]
    },
    "losangeles": {
        "path": 41,
        "row": 36,
        "region": [
            [-118.8, 34.3],
            [-117.5, 34.3],
            [-117.5, 33.5],
            [-118.8, 33.5]
        ]
    }
}

# Parse command line arguments
# Usage: python BuildTimelapse.py region [start_date end_date]
if len(sys.argv) == 4:
    region_key = sys.argv[1].lower()
    start_date = sys.argv[2]
    end_date = sys.argv[3]
elif len(sys.argv) == 2:
    region_key = sys.argv[1].lower()
    start_date = None
    end_date = None
else:
    print("Usage: python BuildTimelapse.py region [start_date end_date]")
    print("Date format: YYYY-MM-DD (e.g., 2015-01-01 2017-12-31)")
    print("Currently supported regions:", list(REGIONS.keys()))
    sys.exit(1)

# Check for valid region
if region_key not in REGIONS:
    print(f"Unknown region: {region_key}")
    print("Currently supported regions:", list(REGIONS.keys()))
    sys.exit(1)

region_info = REGIONS[region_key]

# Filter collection based on region and optional date
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
    .filter(ee.Filter.eq('WRS_PATH', region_info["path"])) \
    .filter(ee.Filter.eq('WRS_ROW', region_info["row"])) \
    .filter(ee.Filter.lt('CLOUD_COVER', 5)) \
    .select(['B4', 'B3', 'B2'])

if start_date and end_date:
    print(f"Generating timelapse for {region_key} from {start_date} to {end_date}")
    collection = collection.filterDate(start_date, end_date)
else:
    print(f"Generating timelapse for {region_key} over all available dates")

# Convert images to 8-bit
def convertBit(image):
    return image.multiply(512).uint8()  

# Given a bounding box, compute dimensions that preserve aspect ratio.
# Returns a string suitable for use in the 'dimensions' parameter.
def compute_dimensions(region_coords, long_side_pixels=720):
    # Get width and height in degrees
    lon_min = min(p[0] for p in region_coords)
    lon_max = max(p[0] for p in region_coords)
    lat_min = min(p[1] for p in region_coords)
    lat_max = max(p[1] for p in region_coords)

    width = lon_max - lon_min
    height = lat_max - lat_min

    if width >= height:
        new_width = long_side_pixels
        new_height = int(round((height / width) * long_side_pixels))
    else:
        new_height = long_side_pixels
        new_width = int(round((width / height) * long_side_pixels))

    return f"{new_width}x{new_height}"



outputVideo = collection.map(convertBit)

image_count = collection.size().getInfo()
print(f"Number of images found: {image_count}")

if image_count == 0:
    print("No images found. Check cloud cover, path/row, or date range.")
    sys.exit(1)


# Export to Google Drive as a video
out = batch.Export.video.toDrive(
    outputVideo,
    description=f'{region_key}_video_timelapse',
    #dimensions=720,
    dimensions=compute_dimensions(region_info["region"]), # Use compute_dimensions helper function
    framesPerSecond=2,
    region=region_info["region"],
    maxFrames=10000
)

batch.Task.start(out)
print("Process sent to cloud")
