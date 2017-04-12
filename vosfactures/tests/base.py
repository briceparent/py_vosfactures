from unittest import TestCase

from vosfactures import settings


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.old_HOST = settings.HOST
        settings.HOST = "testserver.vosfactures.fr"
        cls.old_API_TOKEN = settings.API_TOKEN
        settings.API_TOKEN = "anotsorandomapitoken"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        settings.HOST = cls.old_HOST
        settings.API_TOKEN = cls.old_API_TOKEN
