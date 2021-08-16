# coding=utf-8
from st2common import log as logging
from st2common.runners.base_action import Action
from types import SimpleNamespace
import pymongo


LOG = logging.getLogger(__name__)
COMMIT_STRING = "_st2_commit"


class MongoDatabaseError(Exception):
    pass


class ExecResult(SimpleNamespace):
    def __init__(self, success=True, result=None):
        super().__init__(success=success, result=result)


class MongoClientAction(Action):
    def __init__(self, config, timeout=5):
        super().__init__(config)
        # the pack configuration that will hold the list of mongodb profiles.
        self.config = config
        self.profile_name = None

    def run(self, profile_name):
        super().run()
        self._load_profile(profile_name)
        self.client = pymongo.MongoClient(**self.client_kw)

    def _load_profile(self, profile_name):
        if profile_name is None:
            profile_name = self.config.get("default_profile")

        conf = {}
        if profile_name:
            self.profile_name = profile_name
            for p in self.config["profiles"]:
                if profile_name == p.get("name"):
                    LOG.debug(f"Using '{profile_name}' profile configuration.")
                    conf = p
                    break
            else:
                raise ValueError(
                    f"'{profile_name}' was not found in the pack configuration."
                )

        self.client_kw = {
            "host": conf.get("host"),
            "port": conf.get("port"),
            "replicaSet": conf.get("replica_set"),
            "username": conf.get("username"),
            "password": conf.get("password"),
        }
        if conf.get("enable_tls", True):
            self.client_kw.update(
                {
                    "tls": conf.get("enable_tls", True),
                    "tlsCAFile": conf.get("tls_ca_file"),
                    "tlsCertificateKeyFile": conf.get("tls_key_file"),
                    "tlsAllowInvalidCertificates": conf.get(
                        "tls_allow_invalid_certs", False
                    ),
                    "tlsAllowInvalidHostnames": conf.get(
                        "tls_allow_invalid_hostnames", False
                    ),
                }
            )

    def _db_exists(self, db_name):
        return db_name in self.client.list_database_names()

    def database_list(self):
        """
        Returns a list of available databases.
        """
        res = ExecResult()
        res.result = self.client.list_database_names()
        self.client.close()
        return res

    def database_create(self, name):
        """
        Create a new database using `name`.
        Note: A database is not created until at least 1 document has been created so a commit
              collection and document are created.
        """
        res = ExecResult()
        if not self._db_exists(name):
            db = self.client[name]
            collection = db[COMMIT_STRING]
            collection.insert_one({"name": COMMIT_STRING})
            res.result = f"Database {name} created using profile {self.profile_name}."
        else:
            res.result = (
                f"Database {name} already exists using profile {self.profile_name}."
            )
        self.client.close()
        return res

    def database_delete(self, db_name):
        """
        Delete a database from the mongo server.
        """
        res = ExecResult()
        if self._db_exists(db_name):
            self.client.drop_database(db_name)
            res.result = (
                f"Database {db_name} dropped using profile {self.profile_name}."
            )
        else:
            res.success = False
            res.result = (
                f"Database {db_name} doesn't exist using profile {self.profile_name}."
            )
        self.client.close()
        return res

    def collection_list(self, db_name):
        """
        List available collections in a database
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client[db_name]
            res.result = db.list_collection_names()
            self.client.close()
        else:
            res.success = False
            res.result = (
                f"Database {db_name} doesn't exist using profile {self.profile_name}."
            )
        return res

    def collection_create(self, db_name, name):
        """
        Create a new collection in a database.
        Note: A collection is not created until at least 1 document has been created.
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client[db_name]
            if name not in db.list_collections_names():
                collection = db[name]
                collection.insert_one({"name": COMMIT_STRING})
                res.result = "Collection {} created in {} using profile {}.".format(
                    name, db_name, self.profile_name
                )
            else:
                res.result = (
                    "Collection {} already exists in {} using profile {}.".format(
                        name, db_name, self.profile_name
                    )
                )
        else:
            res.success = False
            res.result = f"Database {db_name} exist using profile {self.profile_name}."
        return res

    def collection_delete(self, db_name, name):
        """
        Drop a collection from a database.
        Note: If the collection is the last in the database then the database is destroyed also.
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client[db_name]
            if name in db.list_collections_names():
                db.drop_collection(name)
                res.result = "Collection {} dropped from {} using profile {}.".format(
                    name, db_name, self.profile_name
                )
            else:
                res.result = (
                    "Collection {} doesn't exist in {} using profile {}.".format(
                        name, db_name, self.profile_name
                    )
                )
        else:
            res.success = False
            res.result = f"Database {db_name} exist using profile {self.profile_name}."

        return res

    def user_create(self, username, password, roles, db_name):
        """
        Create a new user in a database.
        https://docs.mongodb.com/manual/reference/command/createUser/
        Roles: https://docs.mongodb.com/manual/reference/built-in-roles/
            read
            readWrite
            dbAdmin
            dbOwner
            userAdmin
            clusterAdmin
            clusterManager
            clusterMonitor
            hostManager
            backup
            restore
            readAnyDatabase
            readWriteAnyDatabase
            userAdminAnyDatabase
            dbAdminAnyDatabase
            root
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client["admin"]
            res.result = db.command("createUser", username, pwd=password, roles=roles)
            self.client.close()
        else:
            res.success = False
            res.result = f"Database {db_name} doesn't exist using profile {self.profile_name}."
        return res

    def user_update(self, username, db_name, password=None, roles=[], mode="merge"):
        """
        Update an existing user in a database.
        https://docs.mongodb.com/manual/reference/command/updateUser/
        """
        _kwargs = {"roles": roles}
        res = ExecResult()
        if password:
            _kwargs["pwd"] = password

        if self._db_exists(db_name):
            db = self.client[db_name]
            res.result = db.command("updateUser", username, **_kwargs)
        else:
            res.success = False
            res.result = f"Database {db_name} exist using profile {self.profile_name}."

        return res

    def user_list(self, db_name="admin"):
        """
        List the users defined in database.
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client[db_name]

            res.result = db.command("getUsers")
        else:
            res.success = False
            res.result = f"Database {db_name} exist using profile {self.profile_name}."

        return res

    def user_delete(self, db_name, username):
        """
        Delete a given user from a database.
        """
        res = ExecResult()
        if self._db_exists(db_name):
            db = self.client(db_name)
            res.result = db.command("dropUser", username)
        else:
            res.success = False
            res.result = f"Database {db_name} exist using profile {self.profile_name}."
        return res
