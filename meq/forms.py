# from django import forms
# from django.core import validators
# from . import models
#
# class StationForm(forms.ModelForm):
#     class Meta:
#         model = models.Station
#         fields = "__all__"
#         labels={
#             'site_desc':"Site description",
#             'depth':"Depth (m)",
#         }
#         widgets = {
#             'last_modified_by':forms.HiddenInput(),
#         }
#
#
# class SpeciesForm(forms.ModelForm):
#     class Meta:
#         model = models.Species
#         fields = "__all__"
#         widgets = {
#             'last_modified_by':forms.HiddenInput(),
#         }
#
# class SampleForm(forms.ModelForm):
#     class Meta:
#         model = models.Sample
#         exclude = ['date_created','last_modified','season', 'notes_html', 'days_deployed','collector_lines', 'species', 'old_id']
#         labels={
#             'site_desc':"Site description",
#             'samplers':"Samplers"
#         }
#         widgets = {
#             'date_deployed':forms.DateInput(attrs={'type': 'date'}),
#             'date_retrieved':forms.DateInput(attrs={'type': 'date'}),
#             'last_modified_by':forms.HiddenInput(),
#
#         }
#
# class SampleNoteForm(forms.ModelForm):
#     class Meta:
#         model = models.SampleNote
#         fields = "__all__"
#         widgets = {
#             'author':forms.HiddenInput(),
#             'sample': forms.HiddenInput(),
#
#         }
#
#
# class ProbeMeasurementForm(forms.ModelForm):
#     class Meta:
#         fields = ("__all__")
#         model = models.ProbeMeasurement
#         labels={
#             'time_date':"Date / Time (yyyy-mm-dd hh:mm:ss)",
#             'probe_depth':"Probe depth (m)",
#             'probe':"Probe name",
#             'temp_c':"Temp (°C)",
#             'sal_ppt':"Salinity (ppt)",
#             'o2_percent':" Disolved oxygen (%)",
#             'o2_mgl':"Disolved oxygen (mg/l)",
#             'sp_cond_ms':"Specific conductance (mS)",
#             'spc_ms':"Conductivity (mS)",
#             'ph':"pH",
#         }
#
#         widgets = {
#             # 'temp_c':forms.NumberInput(attrs={'placeholder':'°C'}),
#             # 'time_date':forms.DateTimeInput(attrs={'placeholder':'yyyy-mm-dd hh:mm:ss'}),
#             # 'sal_ppt':forms.NumberInput(attrs={'placeholder':'ppt'}),
#             # 'o2_percent':forms.NumberInput(attrs={'placeholder':'%'}),
#             # 'o2_mgl':forms.NumberInput(attrs={'placeholder':'mg/l'}),
#             # 'sp_cond_ms':forms.NumberInput(attrs={'placeholder':'mS'}),
#             # 'spc_ms':forms.NumberInput(attrs={'placeholder':'mS'}),
#             # 'probe_depth':forms.NumberInput(attrs={'placeholder':'m'}),
#             'last_modified_by':forms.HiddenInput(),
#
#         }
#
# class LineCreateForm(forms.ModelForm):
#     number_plates = forms.IntegerField(label='How many plates on this line?', required=False)
#     number_petris = forms.IntegerField(label='How many petri dishes on this line?', required=False)
#
#     class Meta:
#         model = models.Line
#         fields = "__all__"
#         labels={
#             'collector':"DFO collector tag #",
#             'latitude_n':"Latitude (N)",
#             'longitude_w':"Longitude (W)",
#         }
#         widgets = {
#             'latitude_n':forms.NumberInput(attrs={'placeholder':'decimal degrees'}),
#             'longitude_w':forms.NumberInput(attrs={'placeholder':'decimal degrees'}),
#             'notes':forms.Textarea(attrs={'rows':'5'}),
#             'last_modified_by':forms.HiddenInput(),
#             'sample':forms.HiddenInput(),
#         }
#
# class LineForm(forms.ModelForm):
#     class Meta:
#         model = models.Line
#         exclude = ['species',]
#         labels={
#             'collector':"DFO collector tag #",
#             'latitude_n':"Latitude (N)",
#             'longitude_w':"Longitude (W)",
#         }
#         widgets = {
#             'latitude_n':forms.NumberInput(attrs={'placeholder':'decimal degrees'}),
#             'longitude_w':forms.NumberInput(attrs={'placeholder':'decimal degrees'}),
#             'notes':forms.Textarea(attrs={'rows':'5'}),
#             'last_modified_by':forms.HiddenInput(),
#             'sample':forms.HiddenInput(),
#         }
#
# class SurfaceForm(forms.ModelForm):
#     class Meta:
#         model = models.Surface
#         fields = "__all__"
#         exclude = ['species']
#         widgets = {
#             'line':forms.HiddenInput(),
#             'last_modified_by':forms.HiddenInput(),
#         }
#
# class SurfaceImageForm(forms.ModelForm):
#     class Meta:
#         model = models.Surface
#         fields = ('image','last_modified_by')
#         widgets = {
#             'last_modified_by':forms.HiddenInput(),
#         }
#
# class SurfaceSpeciesForm(forms.ModelForm):
#
#     class Meta:
#         model = models.SurfaceSpecies
#         fields = "__all__"
#         labels={
#             'percent_coverage':"Coverage",
#             'notes':"Optional notes",
#         }
#         widgets = {
#             'species':forms.HiddenInput(),
#             'surface':forms.HiddenInput(),
#             'percent_coverage':forms.TextInput(attrs={'placeholder':"Value bewteen 0 and 1"}),
#             'notes': forms.Textarea(attrs={"rows":"3", "placeholder":""}),
#             'last_modified_by':forms.HiddenInput(),
#         }
#
#
# class SampleSpeciesForm(forms.ModelForm):
#     class Meta:
#         model = models.SampleSpecies
#         fields = "__all__"
#         labels={
#             # 'percent_coverage':"Coverage",
#             # 'notes':"Optional notes",
#         }
#         widgets = {
#             'species':forms.HiddenInput(),
#             'sample':forms.HiddenInput(),
#             'observation_date':forms.DateInput(attrs={'type':'date'}),
#             'notes': forms.Textarea(attrs={"rows":"3", "placeholder":""}),
#         }
#
# class LineSpeciesForm(SampleSpeciesForm):
#     class Meta:
#         model = models.LineSpecies
#         fields = "__all__"
#         labels={
#             # 'percent_coverage':"Coverage",
#             # 'notes':"Optional notes",
#         }
#         widgets = {
#             'species':forms.HiddenInput(),
#             'line':forms.HiddenInput(),
#             'observation_date':forms.DateInput(attrs={'type':'date'}),
#             'notes': forms.Textarea(attrs={"rows":"3", "placeholder":""}),
#         }
#
#
# class ReportForm(forms.ModelForm):
#     class Meta:
#         model = models.IncidentalReport
#         exclude = ["season","date_last_modified"]
#
#         labels = {
#             'reporter_name':"Name of person filing report",
#             'notes':"Notes (e.g., habitat, salinity, temperature, etc...) ",
#             'report_date': "Date report received",
#         }
#
#         widgets = {
#             'report_date':forms.DateInput(attrs={'type': 'date'}),
#             'date_of_occurence':forms.DateInput(attrs={'type': 'date'}),
#             'sighting_description': forms.Textarea(attrs={'rows': '3'}),
#             'notes': forms.Textarea(attrs={'rows': '3'}),
#             'last_modified_by':forms.HiddenInput(),
#             # 'species':forms.SelectMultiple(attr={"name":"id_species[]"})
#         }
#
#
