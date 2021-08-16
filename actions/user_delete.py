from lib.base import MongoClientAction


class UserDelete(MongoClientAction):
    """
    Delete an existing database user.

    :profile_name: The name of the profile to use to establish
    """

    def run(self, username, db_name, profile_name=None):
        super().run(profile_name)

        return (True, self.user_delete(username, db_name))
