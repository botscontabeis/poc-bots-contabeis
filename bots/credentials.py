from decouple import config

"""
TODO: criar modelo de credenciais de modo que seja possível:
- atualizar as credenciais sem precisar alterar o código
- ter mais de um conjunto de credenciais por aplicação (?)
"""
UVT_USERNAME = config("UVT_USERNAME")
UVT_PASSWORD = config("UVT_PASSWORD")
