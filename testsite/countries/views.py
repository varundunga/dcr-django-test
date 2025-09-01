from django.http import JsonResponse
from .models import Region


def stats(request):
    regions_data = []
    for region in Region.objects.all():
        countries = region.countries.all()
        regions_data.append({
            "name": region.name,
            "number_countries": countries.count(),
            "total_population": sum(c.population for c in countries)
        })
    response = {"regions": regions_data}

    return JsonResponse(response)
