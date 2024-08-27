import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.resources.models import Country, State, City

class Command(BaseCommand):
    help = 'Load data from CSV files into Country and State models'

    def handle(self, *args, **kwargs):
        # Usar pathlib para construir la ruta del archivo CSV
        countries_csv_path = Path('apps/resources/storage/csv/countries.csv')
        states_csv_path = Path('apps/resources/storage/csv/states.csv')
        cities_csv_path = Path('apps/resources/storage/csv/cities.csv')

        # Cargar datos de países
        with countries_csv_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country, created = Country.objects.update_or_create(
                    country_id=row['id'],
                    name=row['name'],
                    iso3=row['iso3'],
                    iso2=row['iso2'],
                    numeric_code=row['numeric_code'],
                    phone_code=row['phone_code'],
                    capital=row['capital'],
                    currency=row['currency'],
                    currency_name=row['currency_name'],
                    currency_symbol=row['currency_symbol'],
                    tld=row['tld'],
                    timezones=row['timezones'],
                    emoji=row['emoji'],
                    emojiU=row['emojiU'],
                )
                if created:
                    self.stdout.write(f"Country {country.name} created.")
                else:
                    self.stdout.write(f"Country {country.name} already exists.")

        # Cargar datos de estados
        with states_csv_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                state, created = State.objects.update_or_create(
                    name=row['name'],
                    country=row['country_id'],
                    state_code=row['state_code'],
                    type=row['type'],
                )
                if created:
                    self.stdout.write(f"State {state.name} created.")
                else:
                    self.stdout.write(f"State {state.name} already exists.")

        with cities_csv_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                city, created = City.objects.update_or_create(
                    name=row['name'],
                    state_code=row['state_code'],  # Relacionando con el objeto State
                )
                if created:
                    self.stdout.write(f"City {city.name} created.")
                else:
                    self.stdout.write(f"City {city.name} already exists.")