import phonenumbers
from django.http import JsonResponse
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE


def phonenumber_validation_view(request):
    phone_number = request.GET.get("phone", "").replace(" ", "")
    country_code = "DE"  # DEFAULT
    for region_code, country_code_list in COUNTRY_CODE_TO_REGION_CODE.items():
        prefix = f"+{region_code}"
        if phone_number.startswith(prefix):
            country_code = country_code_list[0]
            break
    formater = phonenumbers.AsYouTypeFormatter(country_code)
    result = ""
    for digit in phone_number:
        result = formater.input_digit(digit)
    return JsonResponse(data={"phone": result, "country_code": country_code}, status=201, safe=False)
