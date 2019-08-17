import os, json
from django.http import JsonResponse
from django.views import View
from data import __file__
from django.core.mail import EmailMessage


class SendMailView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            flight_from = self.request.POST.get("flight_from")
            flight_to = self.request.POST.get("flight_to")
            date_from = self.request.POST.get("date_from")
            date_to = self.request.POST.get("date_to")
            amount_passengers = self.request.POST.get("amount_passengers")
            body = "<b>Abflug</b>\n"
            body += f"\t<b>Von: </b>: {flight_from}\n"
            body += f"\t<b>Datum: </b>: {date_from}\n"
            body += "<b>Ankunft</b>\n"
            body += f"\t<b>Nach: </b>: {flight_to}\n"
            body += f"\t<b>Datum: </b>: {date_to}\n"
            body += f"Anzahl Passagiere: {amount_passengers}\n"
            email = EmailMessage("subject", body, to=["mbijou@live.de", "osman_2008@hotmail.de"])
            status = email.send()
            if status == 1:
                return JsonResponse(data={"message": "Email wurde erfolgreich abgesendet", "status": "SUCCESS"},
                                    status=201, safe=False)
            else:
                return JsonResponse(data={"message": "Email konnte nicht abgesendet werden", "status": "FAILURE"},
                                    status=500, safe=False)


def airport_api_view(request):
    with open(os.path.dirname(__file__) + "/airports_output.json", "r") as f:
        json_data = json.load(f)

    with open(os.path.dirname(__file__) + "/german_cities.json", "r") as f:
        cities = json.load(f)

    with open(os.path.dirname(__file__) + "/german_countries.json", "r") as f:
        countries = json.load(f)

    with open(os.path.dirname(__file__) + "/german_names.json", "r") as f:
        airport_names = json.load(f)

    with open(os.path.dirname(__file__) + "/german_iata.json", "r") as f:
        iatas = json.load(f)

    result = []
    q = request.GET.get("q")
    if q is not None and q != "":
        q = q.lower()

        cities = get_cities(q, cities)
        countries = get_countries(q, countries)
        airport_names = get_airport_names(q, airport_names)
        iatas = get_iatas(q, iatas)

        for index in json_data:
            row = json_data[index]
            iata = row.get("iata")

            german_city = row.get("german_city_name")
            german_country = row.get("german_country_name")
            german_airport = row.get("german_name")

            if iata:
                representation = f"{iata} {german_city}, {german_country} - {german_airport}"
            else:
                representation = f"N/A {german_city}, {german_country} - {german_airport}"

            row["representation"] = representation

            representation = representation.lower()

            iata_match = None
            for iata in iatas:
                if representation.startswith(f"{iata} "):
                    result = [row]
                    iata_match = True
                    break

            if iata_match is True:
                break

            order = 0

            for city in cities:
                if representation.startswith(f"{city} ") or representation.endswith(f" {city}") \
                        or f" {city}," in representation:
                    order += 1

            for country in countries:
                if representation.startswith(f"{country} ") or representation.endswith(f" {country}") \
                        or f" {country} " in representation:
                    order += 1

            if order == 1:
                if iata:
                    order = order + 1
                result.append(row)
            elif order == 2:
                if iata:
                    order = order + 1
                    result.insert(0, row)
                else:
                    result.insert(1, row)

            row["order"] = order
    result = result[:10]
    endresult = []
    for row in result:
        endresult.append(row.get("representation"))
    return JsonResponse(data=endresult, status=201, safe=False)


def get_cities(q, cities):
    match_cities = []
    for city in cities:
        city = city.lower()
        if city in q or q in city:
            match_cities.append(city)
    print(match_cities)
    return match_cities


def get_iatas(q, iatas):
    match_iatas = []
    for iata in iatas:
        if iata:
            iata = iata.lower()
        else:
            continue
        for x in q.split(" "):
            if x == iata:
                match_iatas.append(iata)
    print(match_iatas)
    return match_iatas


def get_countries(q, countries):
    match_countries = []
    for country in countries:
        country = country.lower()
        if country in q:
            match_countries.append(country)
    print(match_countries)
    return match_countries


def get_airport_names(q, airport_names):
    match_airport_names = []
    for airport_name in airport_names:
        airport_name = airport_name.lower()
        if airport_name in q:
            match_airport_names.append(airport_name)
    print(match_airport_names)
    return match_airport_names
