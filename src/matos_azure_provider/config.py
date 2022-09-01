from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient

AZURE_CLIENT_MANAGER = {
    "cluster": ContainerServiceClient,
    "instance": ComputeManagementClient,
    "network": NetworkManagementClient,
    "storage": StorageManagementClient,
    "sql": SqlManagementClient
}

AZURE_GROUPED_RESOURCE = {
    "Kubernetes Engine": ['cluster'],
    "Compute": ['instance'],
    "Network": ['network'],
    "Storage": ['storage'],
    "Database": ['sql', 'postgresql'],
    "Monitor": ['monitor'],
    "KeyVault": ['key_vault']
}
