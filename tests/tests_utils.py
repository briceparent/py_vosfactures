from unittest import TestCase
from unittest.mock import patch, MagicMock

from utils import get, delete, post, put, HttpError


class QueryFunctionTest(TestCase):
    def setUp(self):
        self.patcher = patch('utils.requests')
        self.mock_requests = self.patcher.start()
        self.mock_requests.get = MagicMock()
        self.mock_requests.create = MagicMock()
        self.mock_requests.delete = MagicMock()
        self.mock_requests.update = MagicMock()

    def tearDown(self):
        self.patcher.stop()

    def test_json_page_and_action(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        get(json_page="some_page", action='some_action')
        self.mock_requests.get.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )

    def test_url_without_instance(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        get(json_page="some_page", action='some_action')
        self.mock_requests.get.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )

    def test_url_with_instance(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        get(json_page="some_page", action='some_action', instance_id=150)
        self.mock_requests.get.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page/150.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )

    def test_with_data(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        get(json_page="some_page", action='some_action', some="data")
        self.mock_requests.get.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {"some": "data"}}'
        )

    def test_wrong_status_code(self):
        r = MagicMock(status_code=404)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        with self.assertRaises(HttpError):
            get(json_page="some_page", action='some_action')

    def test_get(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.get.return_value = r

        get(json_page="some_page", action='some_action')
        self.mock_requests.get.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )

    def test_post(self):
        r = MagicMock(status_code=201)
        r.json = MagicMock(return_value={})
        self.mock_requests.post.return_value = r

        post(json_page="some_page", action='some_action')
        self.mock_requests.post.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )

    def test_put(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.put.return_value = r

        put(json_page="some_page", action='some_action', new_data="here it is")
        self.mock_requests.put.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {"new_data": "here it is"}}'
        )

    def test_delete(self):
        r = MagicMock(status_code=200)
        r.json = MagicMock(return_value={})
        self.mock_requests.delete.return_value = r

        delete(json_page="some_page", action='some_action', instance_id=12345)
        self.mock_requests.delete.assert_called_with(
            url="https://bricexyz.vosfactures.fr/some_page/12345.json",
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data='{"api_token": "O8un72S5qRgjyFyj30YG/bricexyz", "some_action": {}}'
        )
