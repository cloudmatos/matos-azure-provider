# -*- coding: utf-8 -*-
from typing import Any, Dict
from azure.keyvault.certificates import CertificateClient
from matos_azure_provider.lib import factory
from matos_azure_provider.lib.base_provider import BaseProvider

class AzureKeyVault(BaseProvider):

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct instance service
        """

        self.resource = resource
        super().__init__(**kwargs, client_type="key_vault")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        resources = [item.as_dict() for item in self.conn.vaults.list()]
        resources = [{"type": 'key_vault', 'name': resource['name']} for resource in resources]
        return resources

    def get_resources(self) -> Any: # pylint: disable=R0914
        """
        Fetches instance details.

        Args:
        None
        return: dictionary object.
        """
        resource = None
        for item in self.conn.vaults.list():
            obj_item = self.scrub(item)
            if obj_item.get('name', '') == self.resource.get('name'):
                obj_rg_name = obj_item['id'].split('/')[-5]
                obj_name = obj_item['name']
                obj_item['encrypted_key'] = [self.scrub(fwitem) for fwitem in
                                             self.conn.keys.list(obj_rg_name, obj_name)]
                obj_item['secret_key'] = [self.scrub(fwitem) for fwitem in
                                          self.conn.secrets.list(obj_rg_name, obj_name)]
                uri_name = obj_item['name']
                uri = f"https://{uri_name}.vault.azure.net/"
                cert = CertificateClient(uri, self.credential)
                cert_data = []
                for i in cert.list_properties_of_certificates():
                    var = cert.get_certificate(i.name)
                    key_size = var.policy.key_size
                    key_type = var.policy.key_type
                    action = var.policy.lifetime_actions[0]
                    trasperacy = var.policy.certificate_transparency
                    var1 = {
                        "key_size": key_size,
                        "key_type": key_type.__dict__["_value_"],
                        "action": action.action.__dict__["_value_"],
                        "days_before_expiry": action.days_before_expiry,
                        "lifetime_percentage": action.lifetime_percentage,
                        "transperacy": trasperacy
                    }
                    cert_data.append(var1)
                obj_item['certificates'] = cert_data
                resource = obj_item

        return resource if resource else self.resource


def register() -> Any:
    """Register class plugins

    Returns:
        Any: Nonce
    """
    factory.register("key_vault", AzureKeyVault)
