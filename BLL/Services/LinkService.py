from DAL.Repositories.LinkRepository import LinkRepository


class LinkService:

    def __init__(self, db_session):
        self.session = db_session
        self.link_repo = LinkRepository(self.session)

    def save_deeplinks_to_db(self, deeplinks):

        for deeplink in deeplinks:
            self.link_repo.add_link(deeplink["image"],
                                    deeplink["title"],
                                    deeplink["url"],
                                    deeplink["price"],
                                    deeplink["sale"],
                                    deeplink["group_id"],
                                    deeplink["user_id"])

        self.session.commit()
