from DAL.Repositories.UserRepository import UserRepository


class UserService:

    def __init__(self, db_session):
        self.session = db_session

    def get_user(self, login):

        user_repo = UserRepository(self.session)

        return user_repo.get_user(login)

    def add_user(self, user_data):

        user_repo = UserRepository(self.session)

        return user_repo.add_user(user_data["login"], user_data["password"], user_data["tg_channel"], False,
                                  user_data["vk_token"], user_data["epn_api_token"], user_data["epn_hash"],
                                  int(user_data["start_timer"]), int(user_data["end_timer"]))

    def delete_user(self, user_id):
        return UserRepository(self.session).delete_user(user_id)
