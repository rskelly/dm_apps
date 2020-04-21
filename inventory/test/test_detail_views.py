from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView
from inventory.test import  FactoryFloor
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from .. import views

class TestResourceDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.resource = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_detail', kwargs={"pk":self.resource.pk})
        self.expected_template = 'inventory/resource_detail.html'

    @tag("inventory", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceDetailView, DetailView)

    @tag("inventory", 'detail', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'detail', "context")
    def test_context(self):
        context_vars = [
            "kcount_other",
            "kcount_tc",
            "kcount_cst",
            "kcount_tax",
            "kcount_loc",
            "custodian_count",
            "verified",
            "google_api_key",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)


class TestResourceFullDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.resource = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_full_detail', kwargs={"pk":self.resource.pk})
        self.expected_template = 'inventory/resource_form.html'

    @tag("inventory", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceDetailView, UpdateView)

    @tag("inventory", 'detail', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'detail', "context")
    def test_context(self):
        context_vars = [
            "readonly",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)
        self.assert_value_of_context_var(self.test_url, context_vars)