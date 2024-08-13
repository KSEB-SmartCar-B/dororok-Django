import os

import pandas as pd
from geopy.distance import geodesic


def nearby_sea(region1depth_name, lat, lng):
    redius_km = 5
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'sea_coordinate/sea_coordinate.csv')
    sea_data = pd.read_csv(file_path)
    filtered_sea_data = sea_data[sea_data['지자체'] == region1depth_name]

    user_location = (lat, lng)
    for _, row in filtered_sea_data.iterrows():
        sea_location = (row['lat'], row['lng'])
        distance = geodesic(user_location, sea_location).kilometers
        if distance < redius_km:
            return True
    return False
