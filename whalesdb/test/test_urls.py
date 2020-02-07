from django.urls import reverse, resolve
from django.test import TestCase
from django.utils.translation import activate

from whalesdb import urls, views


class URLTest(TestCase):

    # test that a url signature can be reversed into an address,
    # an address gives an expected signature and the address
    # will link to the expected view or function
    def basic_en_url_test(self, signature, url, view, args=None):
        activate('en')
        en_url = "/en/{}".format(url)

        # Test a URL can be reversed
        if args:
            addr = reverse(signature, args=args)
        else:
            addr = reverse(signature)

        self.assertEqual(addr, en_url)

        # Test the URL can be resolved
        found = resolve(en_url)
        self.assertEqual(found.view_name, signature)

        # Test the resolved URL points to the proper view
        self.assertEqual(found.func.__name__, view.__name__)

    def test_root_url_index_view(self):
        self.basic_en_url_test('whalesdb:index', 'whalesdb/', views.IndexView)

    def test_close_url_close_view(self):
        self.basic_en_url_test('whalesdb:close_me', 'whalesdb/close', views.CloserTemplateView)

    def test_url_create_stn_view(self):
        self.basic_en_url_test('whalesdb:create_stn', 'whalesdb/create/stn', views.CreateStn)

    def test_url_list_stn_view(self):
        self.basic_en_url_test('whalesdb:list_stn', 'whalesdb/list/stn', views.ListStn)

    def test_url_details_stn_view(self):
        self.basic_en_url_test('whalesdb:details_stn', 'whalesdb/details/stn/1', views.DetailsStn, {1})

    def test_url_create_prj_view(self):
        self.basic_en_url_test('whalesdb:create_prj', 'whalesdb/create/prj', views.CreatePrj)

    def test_url_list_prj_view(self):
        self.basic_en_url_test('whalesdb:list_prj', 'whalesdb/list/prj', views.ListPrj)

    def test_url_details_prj_view(self):
        self.basic_en_url_test('whalesdb:details_prj', 'whalesdb/details/prj/1', views.DetailsPrj, {1})

    def test_url_create_mor_view(self):
        self.basic_en_url_test('whalesdb:create_mor', 'whalesdb/create/mor', views.CreateMor)

    def test_url_list_mor_view(self):
        self.basic_en_url_test('whalesdb:list_mor', 'whalesdb/list/mor', views.ListMor)

    def test_url_details_mor_view(self):
        self.basic_en_url_test('whalesdb:details_mor', 'whalesdb/details/mor/1', views.DetailsMor, {1})

    def test_url_save_image_file(self):
        self.basic_en_url_test('whalesdb:save_image', 'whalesdb/img/file.png', views.save_image, {'file.png'})