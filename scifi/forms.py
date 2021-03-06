from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from shared_models import models as shared_models
from . import models

chosen_js_sw = {"class": "chosen-select"}
chosen_js = {"class": "chosen-select-contains"}
multi_select_js = {"class": "multi-select"}


class ResponsibilityCentreForm(forms.ModelForm):
    class Meta:
        model = shared_models.ResponsibilityCenter
        fields = "__all__"
        widgets = {
            "manager": forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        User.objects.all().order_by("last_name", "first_name")]
        USER_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['manager'].choices = USER_CHOICES


class LineObjectForm(forms.ModelForm):
    class Meta:
        model = shared_models.LineObject
        fields = "__all__"


class BusinessLineForm(forms.ModelForm):
    class Meta:
        model = shared_models.BusinessLine
        fields = "__all__"


class AllotmentCodeForm(forms.ModelForm):
    class Meta:
        model = shared_models.AllotmentCode
        fields = "__all__"


class SciFiUserForm(forms.ModelForm):
    class Meta:
        model = models.SciFiUser
        fields = "__all__"
        widgets = {
            "user": forms.Select(attrs=chosen_js),
            "responsibility_centers": forms.SelectMultiple(attrs=multi_select_js),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = shared_models.Project
        fields = "__all__"
        widgets = {
            "default_responsibility_center": forms.Select(attrs=chosen_js),
            "default_allotment_code": forms.Select(attrs=chosen_js),
            "default_business_line": forms.Select(attrs=chosen_js),
            "default_line_object": forms.Select(attrs=chosen_js),
        }


class TransactionForm(forms.ModelForm):
    do_another = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = models.Transaction
        exclude = ["outstanding_obligation"]
        labels = {
            # "fiscal_year": "Fiscal year (SAP style e.g. 2018-2019 = 2019)",
            "consignee_suffix": "Consignee suffix (if left blank, this will be automatically assigned)",
        }
        widgets = {
            # "fiscal_year": forms.Select(attrs=chosen_js_sw),
            "created_by": forms.HiddenInput(),
            "creation_date": forms.DateInput(attrs={"type": "date"}),
            "expected_purchase_date": forms.DateInput(attrs={"type": "date"}),
            "invoice_date": forms.DateInput(attrs={"type": "date"}),
            "responsibility_center": forms.Select(attrs=chosen_js),
            "business_line": forms.Select(attrs=chosen_js),
            "allotment_code": forms.Select(attrs=chosen_js),
            "line_object": forms.Select(attrs=chosen_js),
            "project": forms.Select(attrs=chosen_js),
            "consignee_code": forms.Select(attrs=chosen_js),
        }

    def clean_consignee_suffix(self):
        my_suffix = self.cleaned_data['consignee_suffix']
        my_code = self.cleaned_data['consignee_code']
        my_year = self.cleaned_data['fiscal_year']

        ## it must be exactly 6 chars long
        if my_suffix:
            if len(str(my_suffix)) != 6:
                raise forms.ValidationError("Cosignee suffix must be exactly 6 digits long.")

            ## if must start with the short year. e.g., if fiscal_year_id = 2020, then the suffix must begin with 19####
            if not str(my_suffix).startswith(str(my_year.id - 1)[-2:]):
                raise forms.ValidationError("Since the fiscal year for this transaction is {}, the suffix must begin with {}".format(
                    my_year,
                    str(my_year.id - 1)[-2:],
                ))

        return my_suffix


class CustomTransactionForm(forms.ModelForm):
    do_another = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = models.Transaction
        fields = [
            "fiscal_year",
            "project",
            "responsibility_center",
            "business_line",
            "allotment_code",
            "line_object",
            "supplier_description",
            "expected_purchase_date",
            "obligation_cost",
            "reference_number",
            "consignee_code",
            'consignee_suffix',
            # hidden fields
            "created_by",
            "creation_date",
            "transaction_type",
            "in_mrs",
        ]

        labels = {
            "supplier_description": "Expense description",
            "obligation_cost": "Cost estimation",
            "consignee_suffix": "Consignee suffix (if left blank, this will be automatically assigned)",
        }

        widgets = {
            # "fiscal_year": forms.Select(attrs=chosen_js_sw),
            "responsibility_center": forms.Select(attrs=chosen_js),
            "business_line": forms.Select(attrs=chosen_js),
            "allotment_code": forms.Select(attrs=chosen_js),
            "line_object": forms.Select(attrs=chosen_js),
            "project": forms.Select(attrs=chosen_js),
            "consignee_code": forms.Select(attrs=chosen_js),
            "comment": forms.Textarea(attrs={"rows": 4}),
            "expected_purchase_date": forms.DateInput(attrs={"type": "date"}),

            # hidden because they are given default values
            "created_by": forms.HiddenInput(),
            "creation_date": forms.HiddenInput(),
            "transaction_type": forms.HiddenInput(),
            "in_mrs": forms.HiddenInput(),
        }


class ReportSearchForm(forms.Form):
    report = forms.ChoiceField(required=True)
    fiscal_year = forms.ChoiceField(required=True)
    rc = forms.ChoiceField(required=False, label="Responsibility centre", widget=forms.Select(attrs=chosen_js))
    project = forms.ChoiceField(required=False, label="Project", widget=forms.Select(attrs=chosen_js))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        report_choices = [
            # (1, "Branch Summary"),
            (2, "RC Summary"),
            (3, "Project Summary"),
            (1, "Transaction Export (xlsx)"),
        ]
        report_choices.insert(0, (None, "------"))

        fy_choices = [(obj.id, "{}".format(obj.full)) for obj in shared_models.FiscalYear.objects.all()]
        fy_choices.insert(0, (None, "------"))

        rc_choices = [(obj.id, obj) for obj in shared_models.ResponsibilityCenter.objects.all()]
        rc_choices.insert(0, (None, "------"))

        project_choices = [(obj.id, "{} - {}".format(obj.code, obj.name)) for obj in
                           shared_models.Project.objects.all()]
        project_choices.insert(0, (None, "------"))

        self.fields['report'].choices = report_choices
        self.fields['fiscal_year'].choices = fy_choices
        self.fields['rc'].choices = rc_choices
        self.fields['project'].choices = project_choices
