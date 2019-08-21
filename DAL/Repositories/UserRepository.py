from DAL.Entities.User import User
from DAL.Entities.Group import Group
from DAL.Entities.Link import Link


class UserRepository:

    def __init__(self, db_session):
        self.session = db_session

    def add_user(self, login: str, password: str, tg_channel: str, vk_token: str, epn_api_token: str, epn_hash: str,
                 start_timer: int, end_timer: int):
        return self.session.add(User(login=login, password=password, tg_channel=tg_channel, vk_token=vk_token,
                                     epn_api_token=epn_api_token, epn_hash=epn_hash, start_timer=start_timer,
                                     end_timer=end_timer, last_post_time="0",
                                     post_iteration_counter=0, post_iteration=0))

    def get_user(self, login: str):
        return self.session.query(User).filter(User.login == login).one()

    def delete_user(self, user_id: int):
        self.session.query(Link).filter(Link.user_id == user_id).delete()
        self.session.query(Group).filter(Group.user_id == user_id).delete()
        self.session.query(User).filter(User.id == user_id).delete()
        return 0

    def update_user_password(self, user_data, new_password: str):
        user_data.password = new_password
        return user_data

    def update_user_channel(self, user_data, new_channel: str):
        user_data.tg_channel = new_channel
        return user_data

    def update_user_vk_token(self, user_data, new_vk_token: str):
        user_data.vk_token = new_vk_token
        return user_data

    def update_user_epn_token(self, user_data, new_epn_token: str):
        user_data.epn_token = new_epn_token
        return user_data

    def update_user_start_timer(self, user_data, new_start_timer: int):
        user_data.start_timer = new_start_timer
        return user_data

    def update_user_end_timer(self, user_data, new_end_timer: int):
        user_data.end_timer = new_end_timer
        return user_data

    def update_user_post_iteration(self, user_data, new_post_iteration: int):
        user_data.post_iteration = new_post_iteration
        return user_data
