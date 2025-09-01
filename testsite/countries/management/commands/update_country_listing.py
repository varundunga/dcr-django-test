from django.conf import settings
from django.core.management.base import BaseCommand
import requests

from countries.models import Country, Region


class Command(BaseCommand):
    help = "Loads country data from api."

    API_URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def get_data(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            region, region_created = Region.objects.get_or_create(name=row["region"])
            if region_created:
                self.stdout.write(
                    self.style.SUCCESS("Region: {} - Created".format(region))
                )
            country, country_created = Country.objects.update_or_create(
                name=row["name"],
                defaults={
                    "alpha2Code": row["alpha2Code"],
                    "alpha3Code": row["alpha3Code"],
                    "population": row["population"],
                    "region": region,
                    "topleveldomain": ",".join(row.get("topLevelDomain", [])),
                    "capital": row.get("capital", "")
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "{} - {}".format(
                        country, "Created" if country_created else "Updated"
                    )
                )
            )
