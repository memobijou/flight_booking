import os, json
from django.core.management import BaseCommand
from data import __file__


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.dirname(__file__) + "/test.json") as input_file:
            data = json.load(input_file)

        with open(os.path.dirname(__file__) + "/test_output.json", "w") as output_file:
            json.dump(data, output_file, indent=4, ensure_ascii=False)
