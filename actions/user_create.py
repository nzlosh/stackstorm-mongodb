from lib.base import MongoClient


class UserAdd(MongoClient):
    """
    Add a user to a database.
    """

    def run(self, server_id, zone_name, record_name, response_timeout=5):
        super(UserAdd, self).run(response_timeout)
        try:
            return (True, self.record_get(server_id, zone_name, record_name))
        except PowerDNSClientError as e:
            return (False, "{}".format(e))
