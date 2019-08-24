from DAL.Entities.Link import Link


class LinkRepository:

    def __init__(self, db_session):
        self.session = db_session

    def add_link(self, image: str, title: str, url: str, price: float, sale: int, group_id: int, user_id: int):
        return self.session.add(Link(image=image, title=title, url=url, price=price, sale=sale,
                                     group_id=group_id, user_id=user_id))

    def get_link(self, group_id: int, user_id: int):
        return self.session.query(Link).filter(Link.user_id == user_id
                                               and Link.group_id == group_id).all()[-1]

    def get_all_links(self, group_id: int, user_id: int) -> list:
        return self.session.query(Link).filter(Link.user_id == user_id
                                               and Link.group_id == group_id).all()

