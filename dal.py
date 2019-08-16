import models


class DatabaseAddData:

    def __init__(self, db_session):
        self.session = db_session

    def add_user(self, login: str, password: str, tg_channel: str, vk_token: str, epn_token: str, start_timer: int,
                 end_timer: int):
        return self.session.add(models.User(login=login, password=password, tg_channel=tg_channel, vk_token=vk_token,
                                            epn_token=epn_token, start_timer=start_timer, end_timer=end_timer,
                                            last_post_time="0",
                                            post_iteration_counter=0, post_iteration=0))

    def add_group(self, vk_group_id: str, user_id: int):
        return self.session.add(models.Group(vk_group_id=vk_group_id, user_id=user_id))

    def add_link(self, image: str, title: str, url: str, price: float, sale: int, group_id: int, user_id: int):
        return self.session.add(models.Link(image=image, title=title, url=url, price=price, sale=sale,
                                            group_id=group_id, user_id=user_id))


class DatabaseDeleteData:

    def __init__(self, db_session):
        self.session = db_session

    def delete_link(self, link_id: int):
        return self.session.query(models.Link).filter(models.Link.id == link_id).delete()

    def delete_group(self, group_id: int):
        self.session.query(models.Link).filter(models.Link.group_id == group_id).delete()
        self.session.query(models.Group).filter(models.Group.id == group_id).delete()
        return 0

    def delete_user(self, user_id: int):
        self.session.query(models.Link).filter(models.Link.user_id == user_id).delete()
        self.session.query(models.Group).filter(models.Group.user_id == user_id).delete()
        self.session.query(models.User).filter(models.User.id == user_id).delete()
        return 0


class DatabaseUpdateData:

    def __init__(self, db_session):
        self.session = db_session

    def update_password(self, user_id: int, new_password: str):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'password': new_password})

    def update_channel(self, user_id, new_channel: str):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'tg_channel': new_channel})

    def update_vk_token(self, user_id, new_vk_token: str):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'vk_token': new_vk_token})

    def update_epn_token(self, user_id, new_epn_token: str):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'epn_token': new_epn_token})

    def update_start_timer(self, user_id, new_start_timer: int):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'start_timer': new_start_timer})

    def update_end_timer(self, user_id, new_end_timer: int):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'end_timer': new_end_timer})

    def update_post_iteration(self, user_id, new_post_iteration: int):
        return self.session.query(models.User).filter(models.User.id == user_id).update({'post_iteration': new_post_iteration})


if __name__ == "__main__":
    import json
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    with open('config.json') as json_file:
        db_data = json.load(json_file)["postgresql"]

    engine = create_engine(f"postgresql://{db_data['user']}:{db_data['password']}@{db_data['host']}:{db_data['port']}/"
                           f"{db_data['db']}")

    Session = sessionmaker(bind=engine)
    session = Session()

    # db = DatabaseAddData(session)
    # db.add_user("admin", "admin", "@channel", "3353241", "43334631", 9, 21)
    # db.add_group("-56234345", 4)
    # db.add_link("image_url1", "title_url2", "item_url3", 42.6, 20, 4, 3)

    # db = DatabaseDeleteData(session)
    # db.delete_user(1)
    # db.delete_link(1)
    # db.delete_group(1)

    # db = DatabaseUpdateData(session)
    # db.update_channel(6, "new_channel")
    # db.update_password(6, "new_password")
    # db.update_vk_token(6, "new_vk_token")
    # db.update_epn_token(6, "new_epn_token")
    # db.update_start_timer(6, 7)
    # db.update_end_timer(6, 19)
    # db.update_post_iteration(6, 2)

    session.commit()
    session.close()
