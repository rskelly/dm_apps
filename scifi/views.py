import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Value, TextField, Q, Sum
from django.db.models.functions import Concat
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
###
import os

from lib.functions.fiscal_year import fiscal_year
from lib.functions.nz import nz
from . import models
from . import forms
from . import filters
from . import reports
from . import emails


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'scifi/close_me.html'


def not_in_scifi_group(user):
    if user:
        return user.groups.filter(name='scifi_access').count() != 0


def not_in_scifi_admin_group(user):
    if user:
        return user.groups.filter(name='scifi_admin').count() != 0


class SciFiAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return not_in_scifi_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class SciFiAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return not_in_scifi_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SciFiAccessRequiredMixin, TemplateView):
    template_name = 'scifi/index.html'


# ALLOTMENT CODE #
##################

class AllotmentCodeListView(SciFiAccessRequiredMixin, ListView):
    queryset = models.AllotmentCode.objects.all().order_by("category", "code")


class AllotmentCodeUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.AllotmentCode
    form_class = forms.AllotmentCodeForm
    success_url = reverse_lazy('scifi:allotment_list')


class AllotmentCodeCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.AllotmentCode
    form_class = forms.AllotmentCodeForm
    success_url = reverse_lazy('scifi:digestion_list')


class AllotmentCodeDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.AllotmentCode
    success_url = reverse_lazy('scifi:digestion_list')
    success_message = 'The allotment code was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AllotmentCodeDetailView(SciFiAccessRequiredMixin, DetailView):
    model = models.AllotmentCode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
            'allotment_category',
        ]
        return context


# BUSINESS LINE #
#################

class BusinessLineListView(SciFiAccessRequiredMixin, ListView):
    model = models.BusinessLine


class BusinessLineUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.BusinessLine
    form_class = forms.BusinessLineForm
    success_url = reverse_lazy('scifi:business_list')


class BusinessLineCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.BusinessLine
    form_class = forms.BusinessLineForm
    success_url = reverse_lazy('scifi:business_list')


class BusinessLineDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.BusinessLine
    success_url = reverse_lazy('scifi:business_list')
    success_message = 'The business line was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class BusinessLineDetailView(SciFiAccessRequiredMixin, DetailView):
    model = models.BusinessLine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
        ]
        return context


# LINE OBJECT #
###############

class LineObjectListView(SciFiAccessRequiredMixin, FilterView):
    template_name = 'scifi/lineobject_list.html'
    filterset_class = filters.LineObjectFilter
    model = models.LineObject
    queryset = models.LineObject.objects.annotate(
        search_term=Concat('code', 'name_eng', 'description_eng', output_field=TextField()))


class LineObjectUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.LineObject
    form_class = forms.LineObjectForm
    success_url = reverse_lazy('scifi:lo_list')


class LineObjectCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.LineObject
    form_class = forms.LineObjectForm
    success_url = reverse_lazy('scifi:lo_list')


class LineObjectDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.LineObject
    success_url = reverse_lazy('scifi:lo_list')
    success_message = 'The line object was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class LineObjectDetailView(SciFiAdminRequiredMixin, DetailView):
    model = models.LineObject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name_eng',
            'description_eng',
        ]
        return context


# RC #
######

class ResponsibilityCentreListView(SciFiAccessRequiredMixin, ListView):
    model = models.ResponsibilityCenter


class ResponsibilityCentreUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.ResponsibilityCenter
    form_class = forms.ResponsibilityCentreForm
    success_url = reverse_lazy('scifi:rc_list')


class ResponsibilityCentreCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.ResponsibilityCenter
    form_class = forms.ResponsibilityCentreForm
    success_url = reverse_lazy('scifi:rc_list')


class ResponsibilityCentreDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.ResponsibilityCenter
    success_url = reverse_lazy('scifi:rc_list')
    success_message = 'The RC was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ResponsibilityCentreDetailView(SciFiAccessRequiredMixin, DetailView):
    model = models.ResponsibilityCenter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
            'responsible_manager',
        ]
        return context


# PROJECT #
###########

class ProjectListView(SciFiAccessRequiredMixin, FilterView):
    filterset_class = filters.LineObjectFilter
    template_name = 'scifi/project_list.html'
    queryset = models.Project.objects.annotate(
        search_term=Concat('code', 'name', 'description', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name',
            'code',
            'description',
            'project_lead',
            'default_responsibility_center.code',
            'default_allotment_code.code',
            'default_business_line.code',
            'default_line_object.code',
        ]
        return context


class ProjectUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy('scifi:project_list')


class ProjectCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy('scifi:project_list')


class ProjectDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy('scifi:project_list')
    success_message = 'The project was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ProjectDetailView(SciFiAccessRequiredMixin, DetailView):
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name',
            'code',
            'description',
            'project_lead',
            'default_responsibility_center',
            'default_allotment_code',
            'default_business_line',
            'default_line_object',
        ]
        return context


# TRANSACTION #
###############

class TransactionListView(SciFiAdminRequiredMixin, FilterView):
    template_name = 'scifi/transaction_list.html'
    filterset_class = filters.TransactionFilter
    model = models.Transaction

    # paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'fiscal_year',
            'responsibility_center.code',
            'business_line.code',
            'allotment_code',
            'line_object.code',
            'project.code',
            'transaction_type',
            'supplier_description',
            'creation_date',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'reference_number',
            'invoice_date',
            'in_mrs',
            'amount_paid_in_mrs',
            'mrs_notes',
            'procurement_hub_contact',
            'comment',
        ]
        context["my_object"] = self.model.objects.first()
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {
                "fiscal_year": fiscal_year(),
            }
        return kwargs


class TransactionDetailView(SciFiAdminRequiredMixin, DetailView):
    model = models.Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'fiscal_year',
            'responsibility_center',
            'business_line',
            'allotment_code',
            'line_object',
            'project',
            'transaction_type',
            'supplier_description',
            'creation_date',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'reference_number',
            'invoice_date',
            'in_mrs',
            'amount_paid_in_mrs',
            'mrs_notes',
            'procurement_hub_contact',
            'comment',
        ]
        return context


class TransactionUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.Transaction
    form_class = forms.TransactionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        models.Project.objects.all()]
        context['project_list'] = project_list

        return context


class TransactionCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.Transaction
    form_class = forms.TransactionForm

    def get_initial(self):
        return {
            'created_by': self.request.user,
            'do_another': 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        models.Project.objects.all()]
        context['project_list'] = project_list

        return context

    def form_valid(self, form):
        object = form.save()
        if form.cleaned_data["do_another"] == 1:
            return HttpResponseRedirect(reverse_lazy('scifi:trans_new'))
        else:
            return HttpResponseRedirect(reverse_lazy('scifi:trans_list'))


class TransactionDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.Transaction
    success_url = reverse_lazy('scifi:trans_list')
    success_message = 'The transaction was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


## CUSTOM TRANSACTIONS

class CustomTransactionCreateView(SciFiAccessRequiredMixin, CreateView):
    model = models.Transaction
    form_class = forms.CustomTransactionForm
    template_name = "scifi/transaction_form.html"

    def get_initial(self):
        return {
            'created_by': self.request.user,
            'transaction_type': 1,
            'do_another': 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_transaction'] = True

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        models.Project.objects.all()]
        context['project_list'] = project_list

        # project dict for default coding
        project_dict = {}
        for project in models.Project.objects.all():
            project_dict[project.id] = {}
            project_dict[project.id]["rc"] = project.default_responsibility_center_id
            project_dict[project.id]["bl"] = project.default_business_line_id
            project_dict[project.id]["ac"] = project.default_allotment_code_id
            project_dict[project.id]["lo"] = project.default_line_object_id

        project_json = json.dumps(project_dict)
        # send JSON file to template so that it can be used by js script
        context['project_json'] = project_json

        return context

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewEntryEmail(self.object)
        # send the email object
        if settings.MY_ENVR != 'dev':
            send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                      recipient_list=email.to_list, fail_silently=False, )
        else:
            print('not sending email since in dev mode')
            print(email.from_email)
            print(email.to_list)
            print(email.subject)
            print(email.message)
        messages.success(self.request,
                         "The entry has been submitted and an email has been sent to the branch finance manager!")

        if form.cleaned_data["do_another"] == 1:
            return HttpResponseRedirect(reverse_lazy('scifi:ctrans_new'))
        else:
            return HttpResponseRedirect(reverse_lazy('scifi:index'))


# REPORTS #
###########

class ReportSearchFormView(SciFiAccessRequiredMixin, FormView):
    template_name = 'scifi/report_search.html'
    login_url = '/accounts/login_required/'
    form_class = forms.ReportSearchForm

    def get_initial(self):
        # default the year to the year of the latest samples
        return {
            "fiscal_year": fiscal_year(),
            # "report": 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        fiscal_year = str(form.cleaned_data["fiscal_year"])
        report = int(form.cleaned_data["report"])
        try:
            rc = int(form.cleaned_data["rc"])
        except ValueError:
            rc = None

        if report == 1:
            return HttpResponseRedirect(reverse("scifi:report_branch", kwargs={'fiscal_year': fiscal_year}))
        elif report == 2:
            return HttpResponseRedirect(reverse("scifi:report_rc", kwargs={'fiscal_year': fiscal_year, "rc": rc}))
        # elif report == 3:
        #     return HttpResponseRedirect(reverse("scifi:report_branch", kwargs={'fiscal_year': fiscal_year}))
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("scifi:report_search"))


class BranchSummaryTemplateView(SciFiAccessRequiredMixin, TemplateView):
    template_name = 'scifi/report_branch_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fiscal_year = self.kwargs['fiscal_year']
        context["fiscal_year"] = fiscal_year

        rc_list = [models.ResponsibilityCenter.objects.get(pk=rc["responsibility_center"]) for rc in
                   models.Transaction.objects.filter(fiscal_year=fiscal_year).values(
                       "responsibility_center").order_by("responsibility_center").distinct() if
                   rc["responsibility_center"] is not None]

        context["rc_list"] = rc_list

        # will have to make a custom dictionary to send in
        my_dict = {}
        total_obligations = 0
        total_expenditures = 0
        total_allocations = 0
        total_adjustments = 0

        for rc in rc_list:
            my_dict[rc.code] = {}

            # rc allocation
            try:
                rc_allocations = \
                    models.Transaction.objects.filter(responsibility_center_id=rc.id).filter(
                        fiscal_year=fiscal_year).filter(
                        transaction_type=3).values(
                        "project").order_by("project").distinct().annotate(dsum=Sum("invoice_cost")).first()["dsum"]
            except TypeError:
                rc_allocations = 0

            my_dict[rc.code]["allocations"] = rc_allocations
            # total allocations
            total_allocations += rc_allocations

            # rc adjustments
            try:
                rc_adjustments = \
                    models.Transaction.objects.filter(responsibility_center_id=rc.id).filter(
                        fiscal_year=fiscal_year).filter(
                        transaction_type=2).values(
                        "project").order_by("project").distinct().annotate(dsum=Sum("invoice_cost")).first()["dsum"]
            except TypeError:
                rc_adjustments = 0

            my_dict[rc.code]["adjustments"] = rc_adjustments
            # total allocations
            total_adjustments += rc_adjustments

            # rc obligations
            try:
                rc_obligations = \
                    models.Transaction.objects.filter(responsibility_center_id=rc.id).filter(
                        fiscal_year=fiscal_year).filter(
                        transaction_type=1).values(
                        "project").order_by("project").distinct().annotate(dsum=Sum("outstanding_obligation")).first()[
                        "dsum"]
            except TypeError:
                rc_obligations = 0

            my_dict[rc.code]["obligations"] = rc_obligations
            # total obligations
            total_obligations += rc_obligations

            # rc expenditures
            try:
                rc_expenditures = \
                    models.Transaction.objects.filter(responsibility_center_id=rc.id).filter(
                        fiscal_year=fiscal_year).filter(
                        transaction_type=1).values(
                        "project").order_by("project").distinct().annotate(dsum=Sum("invoice_cost")).first()["dsum"]
            except TypeError:
                rc_expenditures = 0

            my_dict[rc.code]["expenditures"] = rc_expenditures
            # total expenditures
            total_expenditures += rc_expenditures

        my_dict["total_obligations"] = total_obligations
        my_dict["total_expenditures"] = total_expenditures
        my_dict["total_adjustments"] = total_adjustments
        my_dict["total_allocations"] = total_allocations
        context["my_dict"] = my_dict

        return context


class AccountSummaryTemplateView(SciFiAccessRequiredMixin, TemplateView):
    template_name = 'scifi/report_rc_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fiscal_year = self.kwargs['fiscal_year']
        context["fiscal_year"] = fiscal_year

        rc = models.ResponsibilityCenter.objects.get(pk=self.kwargs['rc'])
        context["rc"] = rc

        project_list = [models.Project.objects.get(pk=rc["project"]) for rc in
                        models.Transaction.objects.filter(fiscal_year=fiscal_year).filter(
                            responsibility_center=rc.id).values(
                            "project").order_by("project").distinct() if
                        rc["project"] is not None]
        context["project_list"] = project_list

        ac_list = [models.AllotmentCode.objects.get(pk=rc["allotment_code"]) for rc in
                   models.Transaction.objects.filter(fiscal_year=fiscal_year).filter(
                       responsibility_center=rc.id).values(
                       "allotment_code").order_by("allotment_code").distinct() if
                   rc["allotment_code"]]
        context["ac_list"] = ac_list

        # will have to make a custom dictionary to send in
        my_dict = {}
        total_obligations = {}
        total_expenditures = {}
        total_allocations = {}
        total_adjustments = {}

        for ac in ac_list:
            total_obligations[ac.code] = 0
            total_expenditures[ac.code] = 0
            total_allocations[ac.code] = 0
            total_adjustments[ac.code] = 0

        for p in project_list:
            my_dict[p.code] = {}
            my_dict[p.code]["allocations"] = 0
            my_dict[p.code]["adjustments"] = 0
            my_dict[p.code]["obligations"] = 0
            my_dict[p.code]["expenditures"] = 0
            my_dict[p.code]["rcs"] = str(
                [rc["responsibility_center__code"] for rc in models.Transaction.objects.filter(project=p).values(
                    "responsibility_center__code").order_by("responsibility_center__code").distinct()]).replace("'",
                                                                                                                "").replace(
                "[", "").replace("]", "")
            my_dict[p.code]["ac_cats"] = str([rc["allotment_code__allotment_category__name"] for rc in
                                              models.Transaction.objects.filter(project=p).values(
                                                  "allotment_code__allotment_category__name").order_by(
                                                  "allotment_code").distinct()]).replace("'", "").replace("[",
                                                                                                          "").replace(
                "]", "")

            for ac in ac_list:

                # project allocation
                try:
                    project_allocations = \
                        models.Transaction.objects.filter(project_id=p.id).filter(fiscal_year=fiscal_year).filter(
                            transaction_type=3).filter(allotment_code=ac).values("project").order_by(
                            "project").distinct().annotate(dsum=Sum("invoice_cost")).first()["dsum"]
                except TypeError:
                    project_allocations = 0

                my_dict[p.code]["allocations"] += project_allocations

                # total allocations
                ## must be done by allotment code
                total_allocations[ac.code] += project_allocations

                # project adjustments
                try:
                    project_adjustments = \
                        models.Transaction.objects.filter(project_id=p.id).filter(fiscal_year=fiscal_year).filter(
                            transaction_type=2).filter(allotment_code=ac).values(
                            "project").order_by("project").distinct().annotate(dsum=Sum("invoice_cost")).first()["dsum"]
                except TypeError:
                    project_adjustments = 0

                my_dict[p.code]["adjustments"] += project_adjustments
                # total allocations
                total_adjustments[ac.code] += project_adjustments

                # project obligations
                try:
                    project_obligations = \
                        models.Transaction.objects.filter(project_id=p.id).filter(fiscal_year=fiscal_year).filter(
                            transaction_type=1).filter(allotment_code=ac).values(
                            "project").order_by("project").distinct().annotate(
                            dsum=Sum("outstanding_obligation")).first()[
                            "dsum"]
                except TypeError:
                    project_obligations = 0

                my_dict[p.code]["obligations"] += project_obligations
                # total obligations
                total_obligations[ac.code] += project_obligations

                # project expenditures
                try:
                    project_expenditures = \
                        nz(models.Transaction.objects.filter(project_id=p.id).filter(fiscal_year=fiscal_year).filter(
                            transaction_type=1).filter(allotment_code=ac).values(
                            "project").order_by("project").distinct().annotate(dsum=Sum("invoice_cost")).first()[
                               "dsum"], 0)
                except TypeError:
                    project_expenditures = 0

                my_dict[p.code]["expenditures"] += project_expenditures
                # total expenditures
                total_expenditures[ac.code] += project_expenditures

        my_dict["total_obligations"] = total_obligations
        my_dict["total_expenditures"] = total_expenditures
        my_dict["total_adjustments"] = total_adjustments
        my_dict["total_allocations"] = total_allocations
        context["my_dict"] = my_dict

        return context


class ProjectSummaryListView(SciFiAccessRequiredMixin, ListView):
    template_name = 'scifi/report_project_summary.html'

    def get_queryset(self, **kwargs):
        qs = models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(
            fiscal_year=self.kwargs["fiscal_year"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Transaction.objects.first()
        fy = self.kwargs['fiscal_year']
        context["fiscal_year"] = fy

        project = models.Project.objects.get(pk=self.kwargs['project'])
        context["project"] = project

        context["field_list"] = [
            'fiscal_year',
            'creation_date',
            'allotment_code.allotment_category',
            'transaction_type',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'supplier_description',
        ]

        # will have to make a custom dictionary to send in
        my_dict = {}
        qs = models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(fiscal_year=fy)

        # allocations
        try:
            project_allocations = \
                qs.filter(transaction_type=3).values("project").order_by("project").distinct().annotate(
                    dsum=Sum("invoice_cost")).first()["dsum"]
        except TypeError:
            project_allocations = 0

        my_dict["allocations"] = project_allocations

        # adjustments
        try:
            project_adjustments = \
                qs.filter(transaction_type=2).values("project").order_by("project").distinct().annotate(
                    dsum=Sum("invoice_cost")).first()["dsum"]
        except TypeError:
            project_adjustments = 0

        my_dict["adjustments"] = project_adjustments

        # obligations
        try:
            project_obligations = \
                qs.filter(
                    transaction_type=1).values("project").order_by("project").distinct().annotate(
                    dsum=Sum("outstanding_obligation")).first()["dsum"]
        except TypeError:
            project_obligations = 0

        my_dict["obligations"] = project_obligations

        #  expenditures
        try:
            project_expenditures = \
                qs.filter(transaction_type=1).values("project").order_by("project").distinct().annotate(
                    dsum=Sum("invoice_cost")).first()["dsum"]
        except TypeError:
            project_expenditures = 0

        my_dict["expenditures"] = project_expenditures

        context["my_dict"] = my_dict

        return context


def master_spreadsheet(request, fiscal_year, user=None):
    # my_site = models.Site.objects.get(pk=site)
    file_url = reports.generate_master_spreadsheet(fiscal_year, user)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="Science project planning MASTER LIST {}.xlsx"'.format(
                fiscal_year)
            return response
    raise Http404