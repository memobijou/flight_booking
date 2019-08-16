import re
from django.core.management import BaseCommand
from django.conf import settings
import os
from bs4 import BeautifulSoup


class Command(BaseCommand):
    def src_href_to_django_paths(self, html_content, static_prefix):
        pattern = re.compile(r'(src|href)=\"[^\"]*\"')
        matches = pattern.finditer(html_content)
        for match in matches:
            old = match.group()
            if old.split('="')[1].startswith("http://") or old.split('="')[1].startswith("https://") \
                    or old.split('="')[1].startswith("mailto:") or old.split('="')[1].startswith("#"):
                continue

            if "{% static" in old:
                continue

            new = str(match.group().replace('\"', '\"{% static \'' + static_prefix, 1))
            new = new[:-1]
            new += "\' %}\""
            html_content = html_content.replace(old, new)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.prettify()

    def srcset_to_django_paths(self, html_content, static_prefix):
        pattern = re.compile(r'srcset=\"[^\"]+\"')
        matches = pattern.finditer(html_content)
        for match in matches:
            old = match.group()

            if "{% static" in old:
                continue

            prefix, suffix = old.split('="')[0], old.split('="')[1][:-1]

            srcset = suffix.split(",")
            new_srcset = ""

            for src in srcset:
                src = list(src)
                new_src = ""
                if src[0] == " ":
                    src.remove(" ")
                    new_src = " "
                src = "".join(src)
                src, after_src = src.split(" ")[0], src.split(" ")[1]
                new_src = new_src + "{% static " + "'" + static_prefix + src + "'" + " %} " + after_src
                new_srcset += new_src + ", "
            new_srcset = new_srcset[:-2]  # remove last space and comma
            new = prefix + '="' + new_srcset + '"'
            html_content = html_content.replace(old, new)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.prettify()

    def add_arguments(self, parser):
        parser.add_argument('path', nargs="+", type=str, help='path')
        parser.add_argument('--static_prefix', action="append", type=str, help='Add a prefix to static path', )

    def handle(self, *args, **kwargs):
        paths = kwargs.get("path")
        src_path = settings.BASE_DIR + "/templates/"
        for path in paths:
            src_path += f"/{path}/"

        self.stdout.write(str(paths))

        static_prefix = kwargs["static_prefix"]

        if static_prefix is not None and len(static_prefix) > 0:
            tmp = ""
            for prefix in static_prefix:
                tmp += prefix + "/"

            static_prefix = tmp
        else:
            static_prefix = ""

        self.stdout.write(str(static_prefix))

        for currentpath, dirs, files in os.walk(src_path):
            for file in files:
                file_path = os.path.join(currentpath, file)
                self.stdout.write(file_path)

                with open(file_path, "r") as f:
                    html_content = f.read().replace("\n", "")
                    if "{% load static %}" not in html_content:
                        html_content = "{% load static %}\n" + html_content

                html_content = self.src_href_to_django_paths(html_content, static_prefix)
                html_content = self.srcset_to_django_paths(html_content, static_prefix)

                with open(file_path, "w") as output_f:
                    output_f.write(html_content)
                # self.stdout.write(html_content)

