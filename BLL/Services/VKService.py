import re
import vk
import requests
from DAL.Repositories.GroupRepository import GroupRepository


class VKService:

    def __init__(self, user_data, db_session):
        self.user = user_data
        self.session = db_session

    def get_data_from_vk(self):
        session = vk.Session(access_token=self.user.vk_token)
        api = vk.API(session)
        group_repo = GroupRepository(self.session)

        vk_items = list()

        for group in group_repo.get_all_groups(self.user.id):

            try:
                response = api.wall.get(owner_id=group.vk_group_id, v=5.74, count=8)

                for item in response['items']:
                    if int(self.user.last_post_time) < item['date']:
                        if item['text'] is not "" and item['text'].count('http') == 1:
                            try:
                                url = re.search("(?P<url>https?://[^\s]+)", item["text"]).group("url")
                                text = item['text'].replace(url, '')
                                response = requests.get(url)
                                url = re.findall(r'<meta property="og:url" content=[\'"]?([^\'" >]+)',
                                                 str(response.content))

                                if url[0]:
                                    if "aliexpress.com" in url[0]:
                                        ali_item_id = url[0].split(".html")[0].split("/item/")[1]
                                        vk_items.append([text, ali_item_id, group.id])

                            except:
                                pass
            except Exception:
                pass

        return vk_items
