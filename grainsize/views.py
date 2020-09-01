from .tables import (
    CountryTable,
    ProjectTable,
    AnalysisTable,
    CollectionTable,
    PreservationTable,
    SampleTypeTable,
    StorageTypeTable,
    SampleTable,
    DataTable,
    # FilteredProjectListView
)
from .models import (
    Analysis,
    Collection,
    Country,
    Subregion,
    Data,
    MarineRegion,
    Preservation,
    Project,
    Sample,
    SampleType,
    StorageType,
    Unit)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django_tables2 import SingleTableView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import ProjectFilter

# Create your views here.


def index(request):
    return render(request, 'grainsize/index.html')


# Project
class ProjectSampleList(SingleTableView):
    model = Sample
    template_name = 'grainsize/project_samples.html'
    table_class = SampleTable

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['project'])
        return Sample.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class ProjectListView(SingleTableView):
    model = Project
    table_class = ProjectTable
    template_name = 'grainsize/project_list.html'


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'pi', 'marine_region', 'description']


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'pi', 'marine_region', 'description']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project')


# Sample

class SampleDataList(SingleTableView):
    model = Data
    template_name = 'grainsize/sample_data.html'
    table_class = DataTable

    def get_queryset(self):
        self.sample = get_object_or_404(Sample, pk=self.kwargs['sample'])
        return Data.objects.filter(sample=self.sample)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = self.sample
        return context

class SampleListView(SingleTableView):
    model = Sample
    table_class = SampleTable
    template_name = 'grainsize/sample_list.html'


class SampleDetailView(DetailView):
    model = Sample


class SampleCreate(CreateView):
    model = Sample
    fields = "__all__"


class SampleUpdate(UpdateView):
    model = Sample
    fields = ['project|datetime',
              'datetime',
              'latitude',
              'longitude',
              'analysis',
              'collection',
              'preservation',
              'storage',
              'event_number',
              'start_depth',
              'end_depth',
              'sounding',
              'ancillary_data',
              'unit',
              'sample_id',
              'core',
              'filter',
              'filter_spm',
              'sample_type',
              'comment', ]


class SampleDelete(DeleteView):
    model = Sample
    success_url = reverse_lazy('sample')

# Data

class DataListView(SingleTableView):
    model = Data
    table_class = DataTable
    template_name = 'grainsize/data_list.html'


class DataDetailView(DetailView):
    model = Data


class DataCreate(CreateView):
    model = Data
    fields = ['sample', 'diameter', 'value', ]


class DataUpdate(UpdateView):
    model = Data
    fields = ['sample', 'diameter', 'value', ]


class DataDelete(DeleteView):
    model = Data
    success_url = reverse_lazy('data')


# Country


class CountryListView(SingleTableView):
    model = Country
    table_class = CountryTable
    template_name = 'grainsize/country_list.html'


class CountryDetailView(DetailView):
    model = Country


class CountryCreate(CreateView):
    model = Country
    fields = ['country_name', 'country_code']


class CountryUpdate(UpdateView):
    model = Country
    fields = ['country_name', 'country_code']


class CountryDelete(DeleteView):
    model = Country
    success_url = reverse_lazy('country')


# Analysis
class AnalysisListView(SingleTableView):
    model = Analysis
    table_class = AnalysisTable
    template_name = 'grainsize/analysis_list.html'


class AnalysisDetailView(DetailView):
    model = Analysis


class AnalysisCreate(CreateView):
    model = Analysis
    fields = ['code', 'description']


class AnalysisUpdate(UpdateView):
    model = Analysis
    fields = ['code', 'description']


class AnalysisDelete(DeleteView):
    model = Analysis
    success_url = reverse_lazy('analysis')


# Collection
class CollectionListView(SingleTableView):
    model = Collection
    table_class = CollectionTable
    template_name = 'grainsize/collection_list.html'


class CollectionDetailView(DetailView):
    model = Collection


class CollectionCreate(CreateView):
    model = Collection
    fields = ['code', 'description']


class CollectionUpdate(UpdateView):
    model = Collection
    fields = ['code', 'description']


class CollectionDelete(DeleteView):
    model = Collection
    success_url = reverse_lazy('collection')

# Preservation


class PreservationListView(SingleTableView):
    model = Preservation
    table_class = PreservationTable
    template_name = 'grainsize/preservation_list.html'


class PreservationDetailView(DetailView):
    model = Preservation


class PreservationCreate(CreateView):
    model = Preservation
    fields = ['code', 'description']


class PreservationUpdate(UpdateView):
    model = Preservation
    fields = ['code', 'description']


class PreservationDelete(DeleteView):
    model = Preservation
    success_url = reverse_lazy('preservation')

# SampleType


class SampleTypeListView(SingleTableView):
    model = SampleType
    table_class = SampleTypeTable
    template_name = 'grainsize/sampletype_list.html'


class SampleTypeDetailView(DetailView):
    model = SampleType


class SampleTypeCreate(CreateView):
    model = SampleType
    fields = ['code', 'description']


class SampleTypeUpdate(UpdateView):
    model = SampleType
    fields = ['code', 'description']


class SampleTypeDelete(DeleteView):
    model = SampleType
    success_url = reverse_lazy('sampletype')

# StorageType


class StorageTypeListView(SingleTableView):
    model = StorageType
    table_class = StorageTypeTable
    template_name = 'grainsize/storagetype_list.html'


class StorageTypeDetailView(DetailView):
    model = StorageType


class StorageTypeCreate(CreateView):
    model = StorageType
    fields = ['code', 'container', 'type']


class StorageTypeUpdate(UpdateView):
    model = StorageType
    fields = ['code', 'container', 'type']


class StorageTypeDelete(DeleteView):
    model = StorageType
    success_url = reverse_lazy('storagetype')