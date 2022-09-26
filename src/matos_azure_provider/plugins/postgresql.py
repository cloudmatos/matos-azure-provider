# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_azure_provider.lib import factory
from matos_azure_provider.lib.base_provider import BaseProvider


class AzurePostgreSQL(BaseProvider):

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct instance service
        """

        self.resource = resource
        super().__init__(**kwargs, client_type="postgresql")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        resources = [item.as_dict() for item in self.conn.servers.list()]
        resources = [{"type": 'postgresql', 'name': resource['name'],'rg_name':resource['id'].split('/')[-5]} for resource in resources]
        return resources

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        None
        return: dictionary object.
        """
        resource = None
        resources = [item.as_dict() for item in self.conn.servers.list()]
        resources = [{"type": 'postgresql', 'name': resource['name'],'rg_name':resource['id'].split('/')[-5]} for resource in resources]
        for i in resources:
            servers = self.conn.servers.get(i['rg_name'], i['name']
                                        ).as_dict()
            admin_users = []
            try:
                server_admin = self.conn.server_administrators.get(i['rg_name'], i['name']
                                                                ).as_dict()
                admin_users.append(server_admin)
            except: # pylint: disable=W0702
                pass

            logs = [i.as_dict() for i in self.conn.configurations.list_by_server(
                i['rg_name'], i['name'])]
            resource = [{
                "servers": servers,
                "administrators": admin_users,
                "Logs": logs}]


        return resource if resource else self.resource


def register() -> Any:
    """Register class plugins

    Returns:
        Any: Nonce
    """
    factory.register("postgresql", AzurePostgreSQL)
