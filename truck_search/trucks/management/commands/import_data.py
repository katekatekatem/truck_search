import csv
from decimal import Decimal

from django.core.management.base import BaseCommand

from truck_search.settings import BASE_DIR
from trucks.models import Location, Truck


class Command(BaseCommand):
    help = 'Import data from csv files'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_zips',
            type=str,
            nargs='?',
            default=BASE_DIR / 'trucks/uszips.csv',
            help='The path to the csv file',
        )
        parser.add_argument(
            'csv_trucks',
            type=str,
            nargs='?',
            default=BASE_DIR / 'trucks/trucks.csv',
            help='The path to the csv file',
        )

    def handle(self, *args, **options):
        csv_file_zips = options['csv_zips']
        with open(csv_file_zips, 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                mymodel = Location()
                mymodel.zip = row[0]
                mymodel.latitude = Decimal(row[1])
                mymodel.longitude = Decimal(row[2])
                mymodel.city = row[3]
                mymodel.state = row[5]
                mymodel.save()

        csv_file_trucks = options['csv_trucks']
        with open(csv_file_trucks, 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                mymodel = Truck()
                mymodel.number = row[1]
                mymodel.max_weight = row[2]
                mymodel.location = row[3]
                mymodel.save()
