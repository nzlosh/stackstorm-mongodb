from lib.base import MongoClientAction


class UserCreate(MongoClientAction):
    """
    Create a database user.

    :profile_name: The name of the profile to use to establish
    """

    def run(self, username, password, roles, db_name, profile_name=None):
        super().run(profile_name)

        res = self.user_create(username, password, roles, db_name)
        return (res.success, res.result)
