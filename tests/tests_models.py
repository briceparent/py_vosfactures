from unittest.mock import patch

import settings
from models import Client, Invoice, ObjectIsDeletedError, Product, BaseData, Status, CommandUnavailable
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


class ExampleForbiddenModel(ExampleModel):
    pass


# Unit tests

class BaseDataTest(BaseTestCase):
    # Uses ExampleModel
    test_data = {
            'id': 1, 'title': 'Example title', 'description': "Example description", 'author': "John", 'active': True,
            'creation_date': '2017-04-06T16:26:59.745+02:00'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.AVAILABLE_COMMANDS['ExampleModel'] = ['create', 'get', 'list', 'update', 'delete']
        settings.AVAILABLE_COMMANDS['ExampleForbiddenModel'] = []

    def _get_updated_test_data(self, **kwargs):
        new_test_data = self.test_data.copy()
        new_test_data.update(kwargs)
        return new_test_data

    def test_unavailable_commands_really_forbidden(self):
        with self.assertRaises(CommandUnavailable):
            ExampleForbiddenModel.create()

        with self.assertRaises(CommandUnavailable):
            ExampleForbiddenModel.get(instance_id=1)

        with self.assertRaises(CommandUnavailable):
            ExampleForbiddenModel.list()

        e = ExampleForbiddenModel()
        with self.assertRaises(CommandUnavailable):
            e.update()

        with self.assertRaises(CommandUnavailable):
            e.delete()

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


class InvoiceTest(BaseTestCase):
    test_data = {'id': 1, 'user_id': 1, 'app': None, 'number': '2017-09', 'place': None,
                 'sell_date': '2017-04-07', 'payment_type': None, 'price_net': '797.73', 'price_gross': '952.5',
                 'currency': 'EUR', 'status': 'issued', 'description': None, 'seller_name': 'Facture de test',
                 'seller_tax_no': '123456789', 'seller_street': '', 'seller_post_code': '', 'seller_city': '',
                 'seller_country': '', 'seller_email': '', 'seller_phone': '', 'seller_fax': '', 'seller_www': '',
                 'seller_person': '', 'seller_bank': '', 'seller_bank_account': '', 'buyer_name': 'Travaux.com, test',
                 'buyer_tax_no': '987654321', 'buyer_post_code': '78001', 'buyer_city': 'Stazunis',
                 'buyer_street': 'Av Georges Fitgéralde Kentucky', 'buyer_first_name': 'Sophie', 'buyer_country': 'FR',
                 'created_at': '2017-04-07T17:07:53.000+02:00', 'updated_at': '2017-04-07T17:07:53.000+02:00',
                 'token': 'NP4WXnGNQDu3y2Y4DxUi', 'buyer_email': 'c321@fhdj.com', 'buyer_www': '', 'buyer_fax': '',
                 'buyer_phone': '123456789', 'kind': 'vat', 'pattern': 'nr', 'pattern_nr': 2017, 'pattern_nr_m': None,
                 'pattern_nr_d': None, 'client_id': 1, 'payment_to': '2017-04-08', 'paid': '0.0',
                 'seller_bank_account_id': None, 'lang': 'fr', 'issue_date': '2017-04-07', 'price_tax': '154.77',
                 'department_id': 1, 'correction': None, 'buyer_note': '', 'additional_info_desc': None,
                 'additional_info': False, 'product_cache': 'test, Guide ', 'buyer_last_name': 'Garnier',
                 'from_invoice_id': None, 'oid': None, 'discount': '0.0', 'show_discount': False, 'sent_time': None,
                 'print_time': None, 'recurring_id': None, 'tax2_visible': False, 'warehouse_id': None,
                 'paid_date': None, 'product_id': None, 'issue_year': 2017, 'internal_note': None, 'invoice_id': None,
                 'invoice_template_id': 2413, 'description_long': None, 'buyer_tax_no_kind': '',
                 'seller_tax_no_kind': '', 'description_footer': None, 'sell_date_kind': 'Date limite de validité',
                 'payment_to_kind': 'other_date', 'exchange_currency': None, 'discount_kind': 'percent_total',
                 'income': True, 'from_api': True, 'category_id': None, 'warehouse_document_id': None,
                 'exchange_kind': 'ecb', 'exchange_rate': '1.0', 'use_delivery_address': False, 'delivery_address': '',
                 'accounting_kind': None, 'buyer_person': 'Sophie Garnier', 'buyer_bank_account': '', 'buyer_bank': '',
                 'buyer_mass_payment_code': None, 'exchange_note': '', 'client_company': True, 'buyer_company': True,
                 'show_attachments': False, 'exchange_currency_rate': None, 'has_attachments': False,
                 'exchange_date': None, 'attachments_count': 0, 'delivery_date': '2017-04-07', 'fiscal_status': None,
                 'use_moss': False, 'transaction_date': '2017-04-07', 'email_status': None,
                 'exclude_from_stock_level': False, 'exclude_from_accounting': False, 'exchange_rate_den': '1.0',
                 'exchange_currency_rate_den': '1.0', 'accounting_scheme': None, 'exchange_difference': '0.0',
                 'not_cost': False, 'reverse_charge': False, 'issuer': None, 'use_issuer': False, 'cancelled': False,
                 'recipient_id': None, 'recipient_name': None, 'sales_code': '5246-1976-90146'}

    @patch('models.post')
    def test_create_requires_products(self, _):
        # We refuse the invoices without any products
        with self.assertRaises(ValueError):
            Invoice.create(number="Inv num", title="Invoice #1", issue_date="2017-01-01", department_id=1, client_id=1,
                           positions=[])

    @patch('models.post')
    def test_create_requires_products_by_id(self, _):
        # We don't want to create the products from here, they should be passed with "product_id".
        with self.assertRaises(ValueError):
            Invoice.create(number="Inv num", title="Invoice #1", issue_date="2017-01-01", department_id=1, client_id=1,
                           positions=[{"name": "test", "quantity": 2, "tax": 10, "total_price_gross": 52.5}])

    @patch('models.post')
    def test_extends_BaseData(self, _):
        i = Invoice.create(number="Inv num", title="Invoice #1", issue_date="2017-01-01", department_id=1, client_id=1,
                           positions=[{"product_id": 1, "quantity": 3}])
        self.assertIsInstance(i, BaseData)

    @patch('models.post')
    def test_has_magic_string(self, mock_post):
        mock_post.return_value = self.test_data
        el = Invoice.create(number="Inv num", title="Invoice #1", issue_date="2017-01-01", department_id=1, client_id=1,
                            positions=[{"product_id": 1, "quantity": 3}])
        self.assertEqual(str(el), "1 : 2017-09 (797.73 EUR)")

    @patch('models.get')
    @patch('models.Invoice.update')
    def test_set_status(self, mock_invoice_update, mock_get):
        mock_get.return_value = self.test_data

        el = Invoice.get(instance_id=1)

        self.assertNotEqual(el.status, Status.sent)
        el.set_status(Status.sent)
        self.assertEqual(el.status, Status.sent)
        mock_invoice_update.assert_called_with()
