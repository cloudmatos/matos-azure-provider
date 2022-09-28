from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
AZURE_CLIENT_MANAGER = {
    "cluster": ContainerServiceClient,
    "instance": ComputeManagementClient,
    "network": NetworkManagementClient,
    "storage": StorageManagementClient,
    "sql": SqlManagementClient,
    "key_vault": KeyVaultManagementClient,
    "log_monitor": MonitorManagementClient,
    "postgresql": PostgreSQLManagementClient
}

AZURE_GROUPED_RESOURCE = {
    "Kubernetes Engine": ['cluster'],
    "Compute": ['instance'],
    "Network": ['network'],
    "Storage": ['storage'],
    "Database": ['sql', 'postgresql'],
    "Log_Monitor": ['log_monitor'],
    "KeyVault": ['key_vault'],
}
