from flask import Blueprint
from provider.provider_service.provider_manager import provider_manager


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
        self.add_url_rule('/provider/get', 'Get Provider', self.provider_Obj.get_provider_by_id, methods=['GET'])
