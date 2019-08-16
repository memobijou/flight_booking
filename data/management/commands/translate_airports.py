import os
import json
from data import __file__
import time
import pycountry
from django.core.management import BaseCommand
from googletrans import Translator
translator = Translator()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("STARTED")
        self.translate_airports_json()
        self.stdout.write(self.style.SUCCESS('Finished translation'))

    def translate_airports_json(self):
        countries = {}
        self.stdout.write(os.path.dirname(__file__) + "/airports.json")
        with open(os.path.dirname(__file__) + "/airports.json") as json_file:
            data = json.load(json_file)

        germany_data_length = 0
        for index in data:
            row = data[index]
            if row.get("country") == "DE":
                germany_data_length += 1
        self.stdout.write(str(germany_data_length))
        count = 0
        tmp = 0
        for index in data:
            # self.stdout.write(str(countries))
            row = data[index]
            country_code = row.get("country")
            # self.stdout.write(str(country_code))
            if country_code == "DE":
                german_airport_name = translator.translate(row.get("name"), src="en", dest="de").text
                row["german_name"] = german_airport_name
                self.stdout.write(german_airport_name + " " + str(count) + "/" + str(germany_data_length), ending='\n')
                time.sleep(2)
                german_city_name = translator.translate(row.get("city"), src="en", dest="de").text
                row["german_city_name"] = german_city_name
                time.sleep(2)
                count = count + 1
            else:
                row["german_name"] = row["name"]  # if no german name it defaults to international name
                row["german_city_name"] = row["city"]  # if no german name it defaults to international name

            country_name = getattr(pycountry.countries.get(alpha_2=country_code), "name", country_code)

            if country_code not in countries:
                tmp += 1
                self.stdout.write(str(tmp))
                german_country_name = translator.translate(country_name, src="en", dest="de").text
                countries[country_code] = german_country_name
                time.sleep(2)
            row["country_name"] = country_name
            row["german_country_name"] = countries.get(country_code)

        with open(os.path.dirname(__file__) + "/airports_output.json", "w") as out_file:
                json.dump(data, out_file, indent=4, ensure_ascii=False)
