from DAL.Repositories.LinkRepository import LinkRepository


class LinkService:

    def __init__(self, db_session):
        self.session = db_session

    def save_deeplinks_to_db(self, deeplinks):

        for deeplink in deeplinks:
            try:
                LinkRepository(self.session).add_link(deeplink["image"],
                                                      deeplink["title"],
                                                      deeplink["url"],
                                                      deeplink["price"],
                                                      deeplink["sale"],
                                                      deeplink["group_id"],
                                                      deeplink["user_id"])
            except Exception:
                print(Exception)

        self.session.commit()

    def get_link(self, group, user):
        return LinkRepository(self.session).get_link(group.id, user.id)
