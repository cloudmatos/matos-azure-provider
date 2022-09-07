# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_azure_provider.lib import factory
from matos_azure_provider.lib.base_provider import BaseProvider
from azure.keyvault.certificates import CertificateClient


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

    def get_resources(self) -> Any:
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
                cert = CertificateClient(item.properties.vault_uri, self.credential)
                cert_data = []
                for i in cert.list_properties_of_certificates():
                    var = cert.get_certificate(i.name)
                    cert_data.append(dict(var.policy.__dict__))
                obj_item['certificates'] = cert_data
                resource = obj_item

        return resource if resource else self.resource


def register() -> Any:
    """Register class plugins

    Returns:
        Any: Nonce
    """
    factory.register("key_vault", AzureKeyVault)
