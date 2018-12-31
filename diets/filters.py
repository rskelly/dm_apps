import django_filters
from . import models
from django import forms

class SpeciesFilter(django_filters.FilterSet):
    search_term = django_filters.CharFilter(field_name='search_term', label="Species (any part of name...)", lookup_expr='icontains', widget= forms.TextInput())


#
# class SampleFilter(django_filters.FilterSet):
#     SeasonExact = django_filters.NumberFilter(field_name='year', label="From year", lookup_expr='exact', widget= forms.NumberInput(attrs={'style':"width: 4em"}))
#     MonthExact = django_filters.NumberFilter(field_name='month', label="From month", lookup_expr='exact', widget= forms.NumberInput(attrs={'style':"width: 4em"}))
#
#     class Meta:
#         model = models.Sample
#         fields = {
#             'station':['exact'],
#         }
#
# #
# # class StationFilter(django_filters.FilterSet):
# #     class Meta:
# #         model = models.Station
# #         fields = {
# #             'station_name':['icontains'],
# #             'province':['exact'],
# #         }
# #
# #
#
# class SiteFilter(django_filters.FilterSet):
#     class Meta:
#         model = models.Site
#         fields = {
#             'site':['icontains'],
#             'province':['exact'],
#         }
#
# # class ReportFilter(django_filters.FilterSet):
# #     class Meta:
# #         model = models.IncidentalReport
# #         fields = {
# #             'season':['exact'],
# #             'report_type':['exact'],
# #         }
# #
# #

#
#