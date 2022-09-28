import unittest

from matos_azure_provider.provider import Provider

DUMMY_CREDENTIALS = {
    "tenantId": "",
    "clientId": "",
    "clientSecret": "",
    "subscription_id": ""
}


class TestDiscoveryPlugin(unittest.TestCase):
    """
    Test discovery plugin class
    """
    def setUp(self):
        """Set up data method"""
        self.service_type_map = {
            "cluster": "cluster",
            "instance": "instance",
            "network": "network",
            "sql": "sql",
            "key_vault":"key_vault",
            "log_monitor":"log_monitor",
            "postgresql":"postgresql"
        }

    def test_check_plugins_type_pass(self):
        """Test check plugin type correct"""
        provider = Provider(credentials=DUMMY_CREDENTIALS)
        for key_type, client_type in self.service_type_map.items():
            discovery_service = provider.service_factory.create(
                {"type": key_type, "credentials": DUMMY_CREDENTIALS}
            )
            self.assertEqual(discovery_service.client_type, client_type)


if __name__ == "__main__":
    unittest.main()
