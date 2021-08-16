from lib.base import MongoClientAction


class CollectionList(MongoClientAction):
    """
    List available databases on a mongo server
    """

    def run(self, db_name, profile_name=None):
        super().run(profile_name)

        res = self.collection_list(db_name)

        return (res.success, res.result)
