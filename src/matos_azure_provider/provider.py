# -*- coding: utf-8 -*-
import threading
import logging
from typing import List, Any
from matos_azure_provider.lib.auth import Connection
from matos_azure_provider.plugins import get_package
from matos_azure_provider.lib import factory, loader


logger = logging.getLogger(__name__)


class Provider(Connection):
    """Provider manager

    Args:
        Connection (Class): base connection object
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.credentials = kwargs.get("credentials", None)
        self.application_id = kwargs.get("application_id", None)
        loader.load_plugins(get_package())
        self.service_factory = factory
        self.resource_type = kwargs.get("resource_type")

    def get_assets(self, **kwargs):
        """
        Discover aws resources
        """
        threads = []
        resources = [{"type": "postgresql"}]
        lock = threading.Lock()

        def fetch_discovery_details(rsc_type):
            service_discovery = self.service_factory.create({
                "type": rsc_type,
                "credentials": self.credentials,
                "application_id": self.application_id
            })
            result = service_discovery.get_inventory()
            if result is None:
                return

            with lock:
                if isinstance(result, list):
                    resources.extend(result)
                else:
                    resources.append(result)

        service_map = self.service_factory.fetch_plugins()
        print(service_map)
        for rsc_type, _ in service_map.items():
            if self.resource_type and self.resource_type != rsc_type:
                continue
            thread = threading.Thread(target=fetch_discovery_details, args=(rsc_type,))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
        return resources

    def get_resource_inventory(self, resource):
        """
        Get resource detail data
        """
        return self._get_assets_inventory(resource)

    def get_resource_inventories(self, resource_list: List[Any]):
        """
        Get resources data
        """
        resource_inventories = {}
        lock = threading.Lock()

        def fetch_resource_details(rsc):
            resource_type = rsc.get('type')

            try:
                detail = self._get_assets_inventory(rsc)
                with lock:
                    resource_inventories[resource_type] = [detail] if resource_type not in resource_inventories \
                        else [*resource_inventories[resource_type], detail]
            except Exception as e:
                logger.error(f"{e}")

        threads = []
        for resource in resource_list:
            if self.resource_type and self.resource_type != resource.get("type"):
                continue
            thread = threading.Thread(target=fetch_resource_details, args=(resource,))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        return resource_inventories

    def _get_assets_inventory(self, resource, **kwargs):
        """Get assets inventory method

        Args:
            resource (Object): resource type objects

        Returns:
            Object: cloud resource object
        """
        resource.update({"credentials": self.credentials})
        resource.update({"application_id": self.application_id})
        cloud_resource = self.service_factory.create(resource)
        resource_details = cloud_resource.get_resources()
        if resource_details:
            resource.update(details=resource_details)
        resource.pop("credentials")
        resource.pop("application_id")
        return resource
        