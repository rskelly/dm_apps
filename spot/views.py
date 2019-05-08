import os
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import TextField
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
###
from lib.functions.custom_functions import fiscal_year
from lib.functions.custom_functions import nz
from . import models
from . import forms
from . import filters
from . import reports
from masterlist import models as ml_models


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'spot/close_me.html'


def in_spot_group(user):
    if user:
        return user.groups.filter(name='spot_access').count() != 0


class SpotAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_spot_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_spot_admin_group(user):
    if user:
        return user.groups.filter(name='spot_admin').count() != 0


class SpotAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_spot_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SpotAccessRequiredMixin, TemplateView):
    template_name = 'spot/index.html'


# ORGANIZATION #
################

class OrganizationListView(SpotAccessRequiredMixin, FilterView):
    template_name = 'spot/organization_list.html'
    filterset_class = filters.OrganizationFilter
    model = ml_models.Organization
    queryset = ml_models.Organization.objects.annotate(
        search_term=Concat('name_eng', 'name_fre', 'abbrev', 'id', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = ml_models.Organization.objects.first()
        context["field_list"] = [
            'name_eng',
            'abbrev',
            'province',
            'grouping',
            'regions',
        ]
        return context


#
class OrganizationDetailView(SpotAccessRequiredMixin, DetailView):
    template_name = 'spot/organization_detail.html'
    model = ml_models.Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name_eng',
            'abbrev',
            'address',
            'city',
            'postal_code',
            'province',
            'phone',
            'fax',
            'dfo_contact_instructions',
            'notes',
            'grouping',
            'regions',
            'sectors',
            'date_last_modified',
            'last_modified_by',
        ]
        return context


class OrganizationUpdateView(SpotAccessRequiredMixin, UpdateView):
    template_name = 'spot/organization_form.html'
    model = ml_models.Organization
    form_class = forms.OrganizationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_org = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:org_detail", kwargs={"pk": my_org.id}))


class OrganizationCreateView(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/organization_form.html'
    model = ml_models.Organization
    form_class = forms.OrganizationForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_org = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:org_detail", kwargs={"pk": my_org.id}))


class OrganizationDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/organization_confirm_delete.html'
    model = ml_models.Organization
    success_url = reverse_lazy('spot:org_list')
    success_message = 'The organization was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# MEMBER  (ORGANIZATION MEMBER) #
#################################
class MemberCreateView(SpotAccessRequiredMixin, CreateView):
    model = ml_models.OrganizationMember
    template_name = 'spot/member_form_popout.html'
    login_url = '/accounts/login_required/'
    form_class = forms.MemberForm

    def get_initial(self):
        org = ml_models.Organization.objects.get(pk=self.kwargs['org'])
        return {
            'organization': org,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = ml_models.Organization.objects.get(id=self.kwargs['org'])
        context['organization'] = org

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in ml_models.Person.objects.all()
        ]

        context['person_list'] = person_list

        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))


class MemberUpdateView(SpotAccessRequiredMixin, UpdateView):
    model = ml_models.OrganizationMember
    template_name = 'spot/member_form_popout.html'
    form_class = forms.MemberForm
    login_url = '/accounts/login_required/'

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in ml_models.Person.objects.all()
        ]

        context['person_list'] = person_list

        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user
        }


class MemberDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/member_confirm_delete.html'
    model = ml_models.OrganizationMember
    success_url = reverse_lazy('spot:close_me')
    success_message = 'This member was successfully removed!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# PERSON #
##########

class PersonListView(SpotAccessRequiredMixin, FilterView):
    template_name = 'spot/person_list.html'
    filterset_class = filters.PersonFilter
    model = ml_models.Person
    queryset = ml_models.Person.objects.annotate(
        search_term=Concat('first_name', 'last_name', 'notes', 'id', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = ml_models.Person.objects.first()
        context["field_list"] = [
            'display_name|Last name, First name',
            'phone_1',
            'email_1',
            'organizations',
        ]
        return context


class PersonDetailView(SpotAccessRequiredMixin, DetailView):
    model = ml_models.Person
    template_name = 'spot/person_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'first_name',
            'last_name',
            'phone_1',
            'phone_2',
            'fax',
            'email_1',
            'email_2',
            'notes',
            'last_modified_by',
        ]
        return context


class PersonUpdateView(SpotAccessRequiredMixin, UpdateView):
    model = ml_models.Person
    template_name = 'spot/person_form_popout.html'

    form_class = forms.PersonForm

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("spot:person_detail", kwargs={"pk": self.kwargs["pk"]})


class PersonUpdateViewPopout(SpotAccessRequiredMixin, UpdateView):
    template_name = 'spot/person_form_popout.html'
    model = ml_models.Person
    form_class = forms.PersonForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }


class PersonCreateView(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/person_form.html'
    model = ml_models.Person
    form_class = forms.PersonForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_person = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:person_detail", kwargs={"pk": my_person.id}))


class PersonCreateViewPopout(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/person_form_popout.html'
    model = ml_models.Person
    form_class = forms.PersonForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class PersonDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/person_confirm_delete.html'
    model = ml_models.Person
    success_url = reverse_lazy('spot:person_list')
    success_message = 'The person was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# PROJECT #
###########

class ProjectListView(SpotAccessRequiredMixin, FilterView):
    template_name = 'spot/project_list.html'
    filterset_class = filters.ProjectFilter
    model = models.Project
    queryset = models.Project.objects.annotate(
        search_term=Concat('id', 'title', 'title_abbrev', 'program_reference_number', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["my_object"] = models.Project.objects.first()
        context["field_list"] = [
            'id',
            'path_number',
            'program_reference_number',
            'status',
            'start_year',
            'program.abbrev_eng',
            'organization',
            'title',
            'regions',
        ]
        return context


class ProjectDetailView(SpotAccessRequiredMixin, DetailView):
    template_name = 'spot/project_detail.html'
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_fy"] = fiscal_year()
        context["field_list"] = [
            'id',
            'path_number',
            'program_reference_number',
            'organization',
            'title',
            'program',
            'language',
            'status',
            'regions',
            'start_year',
            'project_length',
            'date_completed',
            'eccc_id',
        ]
        return context


class ProjectUpdateView(SpotAccessRequiredMixin, UpdateView):
    template_name = 'spot/project_form.html'
    model = models.Project
    form_class = forms.ProjectForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_project = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:project_detail", kwargs={"pk": my_project.id}))


class ProjectCreateView(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/project_form.html'
    model = models.Project
    form_class = forms.NewProjectForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_project = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:project_detail", kwargs={"pk": my_project.id}))


class ProjectDeleteView(SpotAdminRequiredMixin, DeleteView):
    template_name = 'spot/project_confirm_delete.html'
    model = models.Project
    success_url = reverse_lazy('spot:project_list')
    success_message = 'The project was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# PROJECT PERSON #
##################
class ProjectPersonCreateView(SpotAccessRequiredMixin, CreateView):
    model = models.ProjectPerson
    template_name = 'spot/project_person_form_popout.html'
    login_url = '/accounts/login_required/'
    form_class = forms.ProjectPersonForm

    def get_initial(self):
        my_project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': my_project,
            'last_modified_by': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_project = models.Project.objects.get(pk=self.kwargs['project'])
        context['project'] = my_project

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in ml_models.Person.objects.all()
        ]

        # get a list of all site users who have not already been connected to ml_models.Person
        person_list_1 = [
            '<a href="#" class="user_insert purple-font" url="{my_url}">{first} {last} (SITE USER)</a>'.format(
                my_url=reverse("spot:user_to_person", kwargs={
                    "user": u.id,
                    "view_name": "project_person_new",
                    "pk": my_project.id,
                }),
                first=u.first_name,
                last=u.last_name,
            ) for u in User.objects.all() if
            u.id not in [p.connected_user_id for p in ml_models.Person.objects.filter(connected_user__isnull=False)]
        ]
        person_list.extend(person_list_1)
        context['person_list'] = person_list

        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))


class ProjectPersonUpdateView(SpotAccessRequiredMixin, UpdateView):
    model = models.ProjectPerson
    template_name = 'spot/project_person_form_popout.html'
    form_class = forms.ProjectPersonForm
    login_url = '/accounts/login_required/'

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse('spot:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get a list of people
        person_list = [
            '<a href="#" class="person_insert" code={id}>{first} {last}</a>'.format(
                id=p.id, first=p.first_name, last=p.last_name
            ) for p in ml_models.Person.objects.all()
        ]

        # get a list of all site users who have not already been connected to ml_models.Person
        person_list_1 = [
            '<a href="#" class="user_insert purple-font" url="{my_url}">{first} {last} (SITE USER)</a>'.format(
                my_url=reverse("spot:user_to_person", kwargs={
                    "user":u.id,
                    "view_name":"project_person_edit",
                    "pk":context['object'].id,
                }),
                first=u.first_name,
                last=u.last_name,
            ) for u in User.objects.all() if u.id not in [p.connected_user_id for p in ml_models.Person.objects.filter(connected_user__isnull=False)]
        ]
        person_list.extend(person_list_1)
        context['person_list'] = person_list
        return context

    def get_initial(self):
        return {
            'last_modified_by': self.request.user
        }


class ProjectPersonDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/project_person_confirm_delete.html'
    model = models.ProjectPerson
    success_url = reverse_lazy('spot:close_me')
    success_message = 'This contact was successfully removed!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def user_to_person(request, user, view_name, pk):
    """
    Adds a user to the masterlist person table
    :param request: HTTP request
    :param user: pk of site user
    :param view_name: should be either 'project_person_new' or 'project_person_edit'
    :param pk: could be pk of project or project person, depending on which view is being called from
    :return: HTTP response
    """
    my_user = User.objects.get(pk=user)
    my_new_person = ml_models.Person.objects.create(
        first_name=my_user.first_name,
        last_name=my_user.last_name,
        connected_user=my_user,
    )
    my_new_person.save()

    # figure out where to go!
    if view_name == "project_person_new":
        target_url = reverse("spot:"+view_name, kwargs={"project":pk})

    elif view_name == "project_person_edit":
        target_url = reverse("spot:"+view_name, kwargs={"pk":pk})

    else:
        target_url= reverse("spot:close_me")

    return HttpResponseRedirect(target_url)

# PROJECT YEAR #
################

class ProjectYearDetailView(SpotAccessRequiredMixin, DetailView):
    template_name = 'spot/project_year_detail.html'
    model = models.ProjectYear

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_fy"] = fiscal_year()
        # send in the name of the project's first fiscal year
        context["first_year"] = fiscal_year()
        # currently field are being called manually into a table. This can be improved when time permits
        context["field_list"] = [
            'annual_funding',
        ]
        context["my_payment"] = models.Payment.objects.first()
        context["payment_field_list"] = [
            # 'project_year',
            'claim_number',
            'disbursement|Total amount',
            'from_period',
            'to_period',
            'final_payment',
            'materials_submitted',
            'nhq_notified',
            'payment_confirmed',
            'notes',
        ]
        return context


class ProjectYearUpdateView(SpotAccessRequiredMixin, UpdateView):
    template_name = 'spot/project_year_form.html'
    model = models.ProjectYear
    form_class = forms.ProjectYearForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:year_detail", kwargs={"pk": my_object.id}))


class ProjectYearCreateView(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/project_year_form.html'
    model = models.ProjectYear
    form_class = forms.ProjectYearForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_project = models.Project.objects.get(pk=self.kwargs['project'])
        context['project'] = my_project
        return context

    def get_initial(self):
        my_project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': my_project,
            'last_modified_by': self.request.user,
        }

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:year_detail", kwargs={"pk": my_object.id}))


class ProjectYearDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/project_year_confirm_delete.html'
    model = models.ProjectYear
    success_message = 'The project year was deleted successfully!'

    def get_success_url(self):
        my_project = models.ProjectYear.objects.get(pk=self.kwargs['pk']).project
        return reverse_lazy('spot:project_detail', kwargs={"pk": my_project.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)



# PAYMENT #
################
class PaymentUpdateView(SpotAccessRequiredMixin, UpdateView):
    template_name = 'spot/payment_form_popout.html'
    model = models.Payment
    form_class = forms.PaymentForm

    def get_initial(self):
        return {'last_modified_by': self.request.user}

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:close_me"))


class PaymentCreateView(SpotAccessRequiredMixin, CreateView):
    template_name = 'spot/payment_form_popout.html'
    model = models.Payment
    form_class = forms.PaymentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_project_year = models.ProjectYear.objects.get(pk=self.kwargs['project_year'])
        context['project_year'] = my_project_year
        return context

    def get_initial(self):
        my_project_year = models.ProjectYear.objects.get(pk=self.kwargs['project_year'])
        if my_project_year.payments.count() == 0:
            claim_number = 1
        else:
            claim_number = my_project_year.payments.count()+1
        return {
            'project_year': my_project_year,
            'last_modified_by': self.request.user,
            'claim_number': claim_number,
        }

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy("spot:close_me"))


class PaymentDeleteView(SpotAccessRequiredMixin, DeleteView):
    template_name = 'spot/payment_confirm_delete.html'
    model = models.Payment
    success_message = 'The payment year was deleted successfully!'

    def get_success_url(self):
        return reverse_lazy('spot:close_me')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
