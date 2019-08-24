from DAL.Entities.User import User
from DAL.Entities.Group import Group
from DAL.Entities.Link import Link


class UserRepository:

    def __init__(self, db_session):
        self.session = db_session

    def add_user(self, login: str, password: str, tg_channel: str, active: bool, vk_token: str, epn_api_token: str,
                 epn_hash: str, start_timer: int, end_timer: int):
        return self.session.add(User(login=login,
                                     password=password,
                                     tg_channel=tg_channel,
                                     active=active,
                                     vk_token=vk_token,
                                     epn_api_token=epn_api_token,
                                     epn_hash=epn_hash,
                                     start_timer=start_timer,
                                     end_timer=end_timer,
                                     last_post_time="0",
                                     post_iteration_counter=0,
                                     post_iteration=0))

    def get_user(self, login: str):
        return self.session.query(User).filter(User.login == login).one()

    def get_all_users(self):
        return self.session.query(User).all()

    def delete_user(self, user_id: int):
        self.session.query(Link).filter(Link.user_id == user_id).delete()
        self.session.query(Group).filter(Group.user_id == user_id).delete()
        self.session.query(User).filter(User.id == user_id).delete()
        return 0
