import unittest

from unittest.mock import Mock

from kaggle_gcp import KaggleKernelCredentials
from test.support import EnvironmentVarGuard
from google.cloud import storage

def _make_credentials():
    import google.auth.credentials
    return Mock(spec=google.auth.credentials.Credentials)

class TestStorage(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(storage.__version__)

    def test_ctr(self):
        credentials = _make_credentials()
        client = storage.Client(project="xyz", credentials=credentials)
        self.assertEqual(client.project, "xyz")

    def test_annonymous_client(self):
        anonymous = storage.Client.create_anonymous_client()
        self.assertIsNotNone(anonymous)

    def test_default_credentials_gcs_enabled(self):
        env = EnvironmentVarGuard()
        env.set('KAGGLE_USER_SECRETS_TOKEN', 'foobar')
        env.set('KAGGLE_KERNEL_INTEGRATIONS', 'GCS')
        with env:
            from sitecustomize import init
            init()
            client = storage.Client(project="xyz")
            self.assertIsInstance(client._credentials, KaggleKernelCredentials)
