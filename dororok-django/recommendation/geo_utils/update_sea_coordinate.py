import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommendation.models import SeaCoordinate



def import_sea_coordinates():
    file_path = 'sea_coordinate/sea_coordinate.csv'

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            SeaCoordinate.objects.create(
                name=row['해수욕장명'],
                local_government=row['지자체'],
                management_agency=row['관리청'],
                beach_name=row['해수욕장명'],
                lat=float(row['lat']),
                lng=float(row['lng'])
            )
        print("Successfully updated sea coordinates")


if __name__ == "__main__":
    import_sea_coordinates()