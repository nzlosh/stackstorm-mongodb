from lib.base import MongoClientAction


class CollectionDelete(MongoClientAction):
    """
    Delete a collection in a database.
    """

    def run(self, db_name, name, profile_name=None):
        super().run(profile_name)

        res = self.collection_delete(db_name, name)

        return (res.success, res.result)
