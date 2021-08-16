from lib.base import MongoClient, MongoDatabaseError


class DatabaseList(MongoClient):
    """
    List available databases on a mongo server
    """

    def run(self, profile_name="default"):
        super().run(profile_name)
        try:
            return (True, self.record_get(server_id, zone_name, record_name))
        except PowerDNSClientError as e:
            return (False, "{}".format(e))
