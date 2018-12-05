import json
import googlemaps

from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.conf import settings

from map.models import Geodata


class Home(TemplateView):
    """
    This is a view function of the homepage.
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context


class GeodataPoints(View):

    def post(self, request):
        """
        The function accepts the request from the click event on the client.
        Checks if there is a point with such data in the local DB.
        If not, send a request to the geocoder,
        checking response for validity
        and saving to the local DB and Google Fusion.

        :param request: {
            csrfmiddlewaretoken: csrftoken,
            lat: float,
            lng: float
        }
        :return: JSON object
        """
        radius_of_inaccuracy = 1/3600  # 1 second of latitude / longitude. Around 31 meters.
        lat = float(request.POST.get("lat", 0))
        lng = float(request.POST.get("lng", 0))

        if lat and lng:
            existing_points = Geodata.objects.filter(latitude__lte=(lat+radius_of_inaccuracy),
                                                     latitude__gte=(lat-radius_of_inaccuracy)).filter(
                                                     longitude__lte=(lng+radius_of_inaccuracy),
                                                     longitude__gte=(lng-radius_of_inaccuracy))

            if existing_points.count():
                response = {'status': 'success', 'message': '', 'data': existing_points.first().getObject()}
            else:
                gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                reverse_geocode_result = gmaps.reverse_geocode((lat, lng))

                if reverse_geocode_result and 'formatted_address' in reverse_geocode_result[0]:
                    if self.validation_of_address(reverse_geocode_result[0]['types']):

                        point = Geodata()
                        point.latitude = lat
                        point.longitude = lng
                        point.address = reverse_geocode_result[0]['formatted_address']
                        point.save()

                        response = {'status': 'success', 'message': '', 'data': point.getObject()}
                    else:
                        response = {'status': 'error', 'message': "Invalid type of point."}
                else:
                    response = {'status': 'error', 'message': "The point doesn't have an address."}
        else:
            response = {'status': 'error', 'message': "Lat or Lng doesn't exist."}

        return HttpResponse(json.dumps(response), content_type="application/json")

    def delete(self, request):
        """
        Delete all points from the database.

        :param request: csrftoken
        :return:
        """
        Geodata.objects.all().delete()
        return HttpResponse(json.dumps('OK'), content_type="application/json")

    def validation_of_address(self, types):
        """
        Checking only of the real address.
        If necessary, add type into verification.

        :param types: list of types location
        :return: Boolean
        """
        return True if 'street_address' in types or 'street_number' in types else False


