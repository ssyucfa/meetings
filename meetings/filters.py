from rest_framework import filters

from meetings.service import calculate_distance


class ClosestFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get("closest_to_me", None)
        if param is None:
            return queryset
        return sorted(
                queryset,
                key=lambda user: calculate_distance(
                    request.user.longitude, request.user.latitude, user.longitude, user.latitude
                )
            )
