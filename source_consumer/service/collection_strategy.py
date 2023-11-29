class CollectionStrategy:

    def __init__(self):
        self.base_name = "similar_docs"

    def get_collection_name_by_tenant(self, tenant_id):
        return f"{self.base_name}_{tenant_id}"
