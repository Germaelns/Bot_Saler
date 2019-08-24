from DAL.Repositories.GroupRepository import GroupRepository


class GroupService:

    def __init__(self, db_session):
        self.session = db_session

    def get_group(self, group_data):
        return GroupRepository(self.session).get_group(group_data["vk_group_id"], group_data["user_id"])

    def get_all_groups_for_user(self, user_id):
        return GroupRepository(self.session).get_all_groups(user_id)

    def add_group(self, group_data):
        return GroupRepository(self.session).add_group(group_data["name"],
                                                       group_data["vk_group_id"],
                                                       group_data["user_id"])

    def delete_group(self, group_id):
        return GroupRepository(self.session).delete_group(group_id)
