from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime
import time

from sqlalchemy.orm.exc import NoResultFound

from BLL.Services.UserService import UserService
from BLL.Services.VKService import VKService
from BLL.Services.EPNService import EPNService
from BLL.Services.LinkService import LinkService
from BLL.Services.TGService import TGService
from BLL.Services.GroupService import GroupService


class BotPostingService:

    def __init__(self, postgres, bot):
        self.db_engine = create_engine(f"postgres://{postgres['user']}:{postgres['password']}@"
                                       f"{postgres['host']}:{postgres['port']}/{postgres['db']}",
                                       pool_pre_ping=True)
        self.bot = bot

    def bot_posting(self):

        while True:
            start_time = time.time()

            session = sessionmaker(bind=self.db_engine)()
            users = UserService(session).get_all_users()

            hour = int(str(datetime.datetime.now().time())[:2])

            if hour == 24:
                hour = 0
            elif hour == 25:
                hour = 1
            elif hour == 26:
                hour = 2

            for user in users:

                if user.active:
                    print(user.login)
                    items = VKService(user, session).get_data_from_vk()
                    deeplinks = EPNService(user).create_deeplinks(items)
                    LinkService(session).save_deeplinks_to_db(deeplinks)

                    user.last_post_time = time.time()
                    session.commit()

                    if int(user.post_iteration_counter) >= int(
                            user.post_iteration) and user.end_timer >= hour >= user.start_timer:
                        groups = GroupService(session).get_all_groups_for_user(user.id)

                        link = list()
                        no_link = False

                        for group in groups:

                            try:
                                link.append(LinkService(session).get_link(group, user))
                                print(link)
                            except NoResultFound:
                                print("no links")
                            except IndexError:
                                print("no links")

                        try:
                            post_data = {
                                "url": link[0].url,
                                "title": link[0].title,
                                "price": link[0].price,
                                "sale": link[0].sale,
                                "image": link[0].image
                            }

                            TGService(user, self.bot).post_to_channel(post_data)
                        except IndexError:
                            pass



            session.close()

            print("waiting...")
            time.sleep(900 - (int(time.time()) - int(start_time)))
