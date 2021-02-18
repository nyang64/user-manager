from flask import Blueprint
from resources.provider_manager import provider_manager


class ProviderBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.provider_Obj = provider_manager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/provider/register',
                          'Register Provider',
                          self.provider_Obj.register_provider,
                          methods=['POST'])
        self.add_url_rule(
            '/provider/get',
            'Get Provider',
            self.provider_Obj.get_provider_by_id, methods=['GET'])
        self.add_url_rule(
            '/provider/delete',
            'Delete the Provider',
            self.provider_Obj.delete_provider, methods=['DELETE'])
        self.add_url_rule(
            '/provider/update',
            'Update the Provider',
            self.provider_Obj.update_provider, methods=['PUT'])
        self.add_url_rule(
            '/providers',
            'Get List of Providers',
            self.provider_Obj.get_providers, methods=['GET'])
