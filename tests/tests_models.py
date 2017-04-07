from unittest.mock import patch

from models import Client, ObjectIsDeletedError, Product, BaseData
from tests.base import BaseTestCase


# Sample model, used to test the behaviours of BaseData

class ExampleModel(BaseData):
    _create_data = dict(json_page="page", action="action")
    _delete_data = dict(json_page="page", action="action")
    _get_data = dict(json_page="page", action="action")
    _list_data = dict(json_page="page", action="actions")
    _update_data = dict(json_page="page", action="action")
    _required_properties = ["title", "author"]
    _auto_data = ['creation_date']
    _default_data = ['active']

    id = None
    title = None
    description = None
    author = None
    active = True
    creation_date = None

    def __str__(self):
        return "{} : {}".format(self.id, self.title)


# Unit tests

class BaseDataTest(BaseTestCase):
    # Uses ExampleModel
    test_data = {
            'id': 1, 'title': 'Example title', 'description': "Example description", 'author': "John", 'active': True,
            'creation_date': '2017-04-06T16:26:59.745+02:00'}

    def _get_updated_test_data(self, **kwargs):
        new_test_data = self.test_data.copy()
        new_test_data.update(kwargs)
        return new_test_data

    @patch('models.get')
    def test_get(self, mock_get):
        mock_get.return_value = self.test_data

        c = ExampleModel.get(instance_id=1)
        mock_get.assert_called_with(json_page='page', action='action', instance_id=1)

        self.assertEqual(c.title, 'Example title')
        self.assertEqual(c.active, True)

    @patch('models.post')
    def test_create(self, mock_post):
        new_title = "A new title"
        mock_post.return_value = self._get_updated_test_data(title=new_title)

        el = ExampleModel.create(title=new_title, author="Henry", active=True)
        mock_post.assert_called_with(json_page='page', action='action', title=new_title, author="Henry", active=True)

        # The create() method returns an ExampleModel instance
        self.assertIsInstance(el, ExampleModel)

        # Its properties have been set correctly
        self.assertEqual(el.title, new_title)

    @patch('models.get')
    @patch('models.delete')
    def test_delete(self, mock_delete, mock_get):
        mock_get.return_value = self.test_data
        mock_delete.return_value = {}

        el = ExampleModel.get(instance_id=1)
        self.assertFalse(el.is_deleted())

        el.delete()
        mock_delete.assert_called_with(json_page='page', action='action', instance_id=1)

        self.assertTrue(el.is_deleted())

    @patch('models.get')
    @patch('models.put')
    def test_update(self, mock_put, mock_get):
        new_title = "Other title"
        mock_get.return_value = self.test_data
        new_element = self.test_data.copy()
        new_element['title'] = new_title
        mock_put.return_value = new_element

        el = ExampleModel.get(instance_id=1)

        self.assertNotEqual(el.title, new_title)
        el.title = new_title
        el.update()
        mock_put.assert_called_with(json_page='page', action='action', id=1, instance_id=1,
                                    active=True, author='John', description='Example description',
                                    title=new_title)

        self.assertEqual(el.title, new_title)

    @patch('models.post')
    def test_default_data_is_added_if_not_set_explicitly_on_creation(self, mock_post):
        new_title = "A new title"
        mock_post.return_value = self._get_updated_test_data(title=new_title)

        el = ExampleModel.create(title=new_title, author="Henry")

        mock_post.assert_called_with(json_page='page', action='action', title=new_title, author="Henry", active=True)

        # Default data should also be assigned to the class
        self.assertTrue(el.active)

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_update_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.test_data
        mock_delete.return_value = {}

        el = ExampleModel.get(instance_id=1)
        el.delete()
        with self.assertRaises(ObjectIsDeletedError):
            el.update()

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_modify_properties_on_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.test_data
        mock_delete.return_value = {}

        el = ExampleModel.get(instance_id=1)
        el.delete()
        with self.assertRaises(ObjectIsDeletedError):
            el.title = "My new title"

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_delete_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.test_data
        mock_delete.return_value = {}

        el = ExampleModel.get(instance_id=6346560)
        el.delete()
        with self.assertRaises(ObjectIsDeletedError):
            el.delete()


class ClientTest(BaseTestCase):
    test_data = {
            'id': 1, 'name': 'Company name', 'tax_no': "123456", 'post_code': None, 'city': None,
            'street': None, 'first_name': None, 'country': None, 'email': None, 'phone': None, 'www': None, 'fax': None,
            'created_at': '2017-04-06T16:26:59.745+02:00', 'updated_at': '2017-04-06T16:26:59.745+02:00',
            'street_no': None, 'kind': 'buyer', 'bank': None, 'bank_account': None, 'bank_account_id': None,
            'shortcut': 'Company name for Get (4)', 'note': None, 'last_name': None, 'password_hash': None,
            'referrer': None, 'password_salt': None, 'token': 'WGye54sLIekJWgddsYfh', 'fuid': None, 'fname': None,
            'femail': None, 'dynamic_fields': {}, 'deleted': False, 'department_id': None, 'import': None,
            'discount': None, 'payment_to_kind': None, 'category_id': None, 'use_delivery_address': False,
            'delivery_address': None, 'person': None, 'panel_user_id': None, 'use_mass_payment': False,
            'mass_payment_code': None, 'external_id': None, 'company': True, 'title': None, 'mobile_phone': None,
            'register_number': None, 'tax_no_check': None, 'attachments_count': 0, 'default_payment_type': None,
            'tax_no_kind': None, 'accounting_id': None, 'disable_auto_reminders': False, 'buyer_id': None}

    @patch('models.post')
    def test_extends_BaseData(self, _):
        self.assertIsInstance(Client.create(name="Ha"), BaseData)

    @patch('models.post')
    def test_has_magic_string(self, mock_post):
        mock_post.return_value = self.test_data
        el = Client.create(name="Customer name")
        self.assertEqual(str(el), "Company name (1)")


class ProductTest(BaseTestCase):
    test_data = {
        'id': 1, 'name': 'Test product', 'description': 'Some description', 'price_net': '250.0', 'tax': '20',
        'created_at': '2017-04-05T16:25:26.000+02:00', 'updated_at': '2017-04-05T16:25:26.000+02:00',
        'automatic_sales': False, 'limited': False, 'warehouse_quantity': '0.0', 'available_from': None,
        'available_to': None, 'payment_callback': None, 'payment_url_ok': None, 'payment_url_error': None,
        'token': 'M4YlfF9ax4XOTAAhlDB', 'quantity': '1.0', 'quantity_unit': 'pc', 'additional_info': '',
        'disabled': False, 'price_gross': '300.0', 'price_tax': '50.0', 'form_fields_horizontal': True,
        'form_fields': None, 'form_name': 'Guide de test', 'form_description': '', 'quantity_sold_outside': None,
        'form_kind': 'default', 'form_template': None, 'elastic_price': False, 'next_product_id': None,
        'quantity_sold_in_invoices': '1.0', 'deleted': False, 'code': 'GDP1', 'currency': 'EUR', 'ecommerce': False,
        'period': None, 'show_elastic_price': False, 'elastic_price_details': None, 'elastic_price_date_trigger': None,
        'iid': None, 'purchase_price_net': None, 'purchase_price_gross': None, 'use_formula': False, 'formula': None,
        'formula_test_field': None, 'stock_level': '-1.0', 'sync': False, 'category_id': None, 'kind': 'sell',
        'package': False, 'package_product_ids': None, 'department_id': None, 'use_product_warehouses': False,
        'purchase_price_tax': None, 'purchase_tax': None, 'service': False, 'use_quantity_discount': False,
        'quantity_discount_details': None, 'price_net_on_payment': False, 'warehouse_numbers_updated_at': None,
        'ean_code': None, 'weight': None, 'weight_unit': None, 'size_height': None, 'size_width': None, 'size': None,
        'size_unit': None, 'auto_payment_department_id': None, 'attachments_count': 0, 'image_url': None, 'tax2': '0',
        'purchase_tax2': '0', 'supplier_code': None, 'package_products_details': None, 'siteor_disabled': False,
        'use_moss': False, 'subscription_id': None, 'accounting_id': None}

    @patch('models.post')
    def test_extends_BaseData(self, _):
        self.assertIsInstance(Product.create(name="Prod", price_net=1, tax=1), BaseData)

    @patch('models.post')
    def test_has_magic_string(self, mock_post):
        mock_post.return_value = self.test_data
        el = Product.create(name="Prod", price_net=1, tax=1)
        self.assertEqual(str(el), "1 : Test product (250.0 EUR)")
