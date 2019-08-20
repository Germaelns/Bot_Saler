import re
import vk
from DAL.Repositories.GroupRepository import GroupRepository


class VKService:

    def __init__(self, user_data, db_session):
        self.user = user_data
        self.session = db_session

    def get_data_from_vk(self):
        session = vk.Session(access_token=self.user.vk_token)
        api = vk.API(session)

        post_data = list()

        last_post_time = float(self.user.last_post_time)

        groups = GroupRepository(self.session)

        for group in groups.get_all_groups(self.user.id):

            response = api.wall.get(owner_id=group.vk_group_id, v=5.74, count=5)
