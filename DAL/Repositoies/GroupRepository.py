from DAL.Entities.Group import Group
from DAL.Entities.Link import Link


class GroupRepository:

    def __init__(self, db_session):
        self.session = db_session

    def add_group(self, vk_group_id: str, user_id: int):
        return self.session.add(Group(vk_group_id=vk_group_id, user_id=user_id))

    def get_group(self, vk_group_id: str, user_id: int):
        return self.session.query(Group).filter(Group.vk_group_id == vk_group_id
                                                and user_id == user_id).one()

    def get_all_groups(self, user_id: int) -> list:
        return self.session.query(Group).filter(Group.user_id == user_id).all()

    def delete_group(self, group_id: int):
        self.session.query(Link).filter(Link.group_id == group_id).delete()
        self.session.query(Group).filter(Group.id == group_id).delete()
        return 0
