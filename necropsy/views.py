from lib.functions.custom_functions import listrify
from shared_models import models as shared_models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from . import models
from . import forms
from . import filters
from . import reports

class CloserTemplateView(TemplateView):
    template_name = 'necropsy/close_me.html'


def in_vault_group(user):
    if user:
        return True


class VaultAccessRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_vault_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_vault_group, login_url='/accounts/denied/')
def index(request):
    return render(request, 'necropsy/index.html')

# #
# # INVENTORY #
# # ###########
# #
#
class ItemListView(VaultAccessRequired, FilterView):
    template_name = "necropsy/item_list.html"
    filterset_class = filters.ItemFilter
    queryset = models.Item.objects.annotate(
        search_term=Concat('id', 'unique_id', 'item_name', 'description', 'owner', 'size', 'container_space', 'category', 'type', output_field=TextField()))

class ItemDetailView(VaultAccessRequired, DetailView):
    model = models.Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'unique_id',
            'item_name',
            'description',
            'owner',
            'size',
            'container_space',
            'category',
            'type',
        ]
        return context

class ItemUpdateView(VaultAccessRequired, UpdateView):
    model = models.Item
    form_class = forms.ItemForm

    def form_valid(self, form):
        messages.success(self.request, _("Item record successfully updated for : {}".format(self.object)))
        return super().form_valid(form)

class ItemCreateView(VaultAccessRequired, CreateView):
    model = models.Item
    form_class = forms.ItemForm

    def form_valid(self, form):
        messages.success(self.request, _("Item record successfully created for : {}".format(self.object)))
        return super().form_valid(form)

class ItemDeleteView(VaultAccessRequired, DeleteView):
    model = models.Item
    permission_required = "__all__"
    success_url = reverse_lazy('necropsy:item_list')
    success_message = 'The item was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)