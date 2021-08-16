from lib.base import MongoClientAction


class CollectionCreate(MongoClientAction):
    """
    Create a new collection in a database.
    """

    def run(self, db_name, name, profile_name=None):
        super().run(profile_name)

        res = self.collection_create(db_name, name)

        return (res.success, res.result)
