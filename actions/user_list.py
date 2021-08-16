from lib.base import MongoClientAction


class UserUpdate(MongoClientAction):
    """
    List users in a database.

    :profile_name: The name of the profile to use to establish
    """

    def run(self, db_name, profile_name=None):
        super().run(profile_name)

        res = self.user_list(db_name)

        return (res.success, res.result)
