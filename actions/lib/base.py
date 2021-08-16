# coding=utf-8
from st2common import log as logging
from st2common.runners.base_action import Action
import pymongo


LOG = logging.getLogger(__name__)


class MongoDatabaseError(Exception):
    pass


class MongoClient(Action):
    def __init__(self, config, timeout=5):
        super(MongoClient, self).__init__(config)
        # the pack configuration that will hold the list of mongodb profiles.
        self.config = config

    def run(
        self,
        db_host,
        db_port,
        db_name,
        db_username,
        db_password,
        enable_tls=False,
        enable_tz_awareness=False,
    ):
        super().run()
        self.client = pymongo.MongoClient(
            host=db_host, port=db_port, tls=enable_tls, tz_aware=enable_tz_awareness
        )

    def _database_present(self, db_name):
        if db_name not in self.client.list_database_names():
            raise MongoDatabaseError(f"Database {db_name} doesn't exist.")

    def database_list(self):
        """
        Returns a list of available databases.
        """
        return self.client.list_datbase_names()

    def database_create(self, name):
        """
        Create a new database using `name`.
        Note: A database is not created until at least 1 document has been created so a dummy collection and document are created then deleted.
        """
        db = self.client[name]
        collection = db["dummy"]
        fake = collection.insert_one({"name": "dummy"})
        collection.delete_one({"name": "dummy"})
        return True

    def database_delete(self, db_name):
        self.client.drop_database(db_name)
        return True

    def collection_list(self, db_name):
        """
        List available collections in a database
        """
        raise NotImplementedError

    def collection_create(self, db_name, name):
        """
        Create a new collection in a database.
        Note: A collection is not created until at least 1 document has been created.
        """
        self._database_present(db_name)

        db = self.client[db_name]
        collection = db[name]

    def collection_delete(self):
        raise NotImplementedError

    def user_add(self):
        raise NotImplementedError

    def user_list(self):
        raise NotImplementedError

    def user_delete(self):
        raise NotImplementedError
