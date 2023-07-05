from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework import filters


class DistanceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        distance = request.query_params.get('distance')
        user_longitude = request.user.longitude
        user_latitude = request.user.latitude

        if user_longitude and user_latitude and distance:

            # calculate the distance formula expression
            expression = (
                ACos(
                    Cos(Radians(user_latitude)) *
                    Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - Radians(user_longitude)) +
                    Sin(Radians(user_latitude)) *
                    Sin(Radians(F('latitude')))
                ) * 6373  # Approximate radius of earth in km
            )

            # apply the distance filter
            queryset = queryset.annotate(
                distance=expression).filter(distance__lte=distance)

        return queryset
