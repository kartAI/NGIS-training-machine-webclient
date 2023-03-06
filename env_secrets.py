config = {
    "AZURE_BYGG_POSTGRESQL_PSW": "Io4$7M1e",
    "NK_WMS_API_KEY": "4A533207-1AC4-44ED-AD52-C89873BD6BD1",
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=buildingdetectionmodels;AccountKey=KAfv7yYGkvNqPA1mctxPv0aXOHJ3B2CICiPCNQzWLu5IxwmqN/ROyoEZ4XpX6d6MPTeu+0yZKFC5CRk8e85P2A==;EndpointSuffix=core.windows.net",
            "NK_POSTGRESQL_PWD": "", 
}
def get_env_secret(variable): 
    return config[variable]
