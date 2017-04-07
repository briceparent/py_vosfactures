from unittest.mock import patch

from models import Client, ObjectIsDeletedError
from tests.base import BaseTestCase


class ClientTest(BaseTestCase):
    client_test_data = {
            'id': 6346560, 'name': 'Company name', 'tax_no': "123456", 'post_code': None, 'city': None,
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

    @patch('models.get')
    def test_get(self, mock_get):
        mock_get.return_value = self.client_test_data

        c = Client.get(instance_id=6346560)
        mock_get.assert_called_with(action='client', instance_id=6346560, json_page='clients')

        self.assertEqual(c.name, "Company name")
        self.assertEqual(c.tax_no, "123456")
        self.assertIsNone(c.tax_no_check)

    @patch('models.post')
    def test_create(self, mock_post):
        mock_post.return_value = self.client_test_data

        c = Client.create(name="Company name for Create")
        mock_post.assert_called_with(action='client', name='Company name for Create', json_page='clients')

        # The create() method returns a Client instance
        self.assertIsInstance(c, Client)

        # Its properties have been set correctly
        self.assertEqual(c.name, "Company name")

    @patch('models.get')
    @patch('models.delete')
    def test_delete(self, mock_delete, mock_get):
        mock_get.return_value = self.client_test_data
        mock_delete.return_value = {}

        c = Client.get(instance_id=6346560)
        self.assertFalse(c.is_deleted())

        c.delete()
        mock_delete.assert_called_with(action='client', instance_id=6346560, json_page='clients')

        self.assertTrue(c.is_deleted())

    @patch('models.get')
    @patch('models.put')
    def test_update(self, mock_put, mock_get):
        mock_get.return_value = self.client_test_data
        new_client = self.client_test_data.copy()
        new_client['post_code'] = "98765"
        mock_put.return_value = new_client

        c = Client.get(instance_id=6346560)

        self.assertNotEqual(c.post_code, new_client['post_code'])
        c.post_code = new_client['post_code']
        c.update()
        mock_put.assert_called_with(action='client', company=True, id=6346560, instance_id=6346560, json_page='clients',
                                    name='Company name', tax_no='123456', post_code=new_client['post_code'])

        self.assertEqual(c.post_code, new_client['post_code'])

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_update_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.client_test_data
        mock_delete.return_value = {}

        c = Client.get(instance_id=6346560)
        c.delete()
        with self.assertRaises(ObjectIsDeletedError):
            c.update()

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_modify_properties_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.client_test_data
        mock_delete.return_value = {}

        c = Client.get(instance_id=6346560)
        c.delete()
        with self.assertRaises(ObjectIsDeletedError):
            c.first_name = "My name"

    @patch('models.delete')
    @patch('models.get')
    def test_test_cant_delete_a_deleted_object(self, mock_get, mock_delete):
        mock_get.return_value = self.client_test_data
        mock_delete.return_value = {}

        c = Client.get(instance_id=6346560)
        c.delete()
        with self.assertRaises(ObjectIsDeletedError):
            c.delete()
