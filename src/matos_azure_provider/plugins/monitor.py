# -*- coding: utf-8 -*-
from typing import Any, Dict
from azure.mgmt.resource import ResourceManagementClient
from matos_azure_provider.lib import factory
from matos_azure_provider.lib.base_provider import BaseProvider

class AzureMonitor(BaseProvider):

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct instance service
        """

        self.resource = resource
        super().__init__(**kwargs, client_type="log_monitor")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        client = ResourceManagementClient(self.credential,self.subscription_id)
        resources = [item.as_dict() for item in client.resource_groups.list()]
        resources = [{"type": 'log_monitor', 'name': resource['name']} for resource in resources]
        return resources

    def get_resources(self) -> Any:
        """
        Fetches instance details.

        Args:
        None
        return: dictionary object.
        """
        resource_ = None
        client = ResourceManagementClient(self.credential,self.subscription_id)
        resources = [{"type": 'log_monitor', 'name': item.name,'location': item.location}
                     for item in client.resource_groups.list()]
        for i in resources:
            data = {}
            resource = [item.as_dict() for item in self.conn.activity_log_alerts.list_by_resource_group(
            i['name'])]
            data['name'] = i['name']
            data['location'] = i['location']
            data['alerts'] = resource
            resource_ = data
        return resource_ if resource_ else self.resource


def register() -> Any:
    """Register class plugins

    Returns:
        Any: Nonce
    """
    factory.register("log_monitor", AzureMonitor)
