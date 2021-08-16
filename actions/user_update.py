from lib.base import MongoClientAction


class UserUpdate(MongoClientAction):
    """
    Update an existing database user account.

    :profile_name: The name of the profile to use to establish
    """

    def run(self, username, password, profile_name=None):
        super().run(profile_name)

        return (True, self.user_create(username, password, roles, db_name, mode))
