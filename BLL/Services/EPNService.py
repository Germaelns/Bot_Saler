import requests
import json


class EPNService:

    def __init__(self, user, group):
        self.user = user
        self.group = group

    def create_deeplinks(self, vk_items: list):

        deeplinks = list()

        for item in vk_items:
            data = {
                "user_api_key": "" + self.user.epn_api_token,
                "user_hash": "" + self.user.epn_hash,
                "api_version": 1,
                "requests": {
                    "request_1": {
                        "action": "offer_info",
                        "lang": "ru",
                        "id": "" + item[1],
                        "currency": "USD"

                    }
                }
            }
            headers = {
                'Content-Type': 'application/json'
            }
            responce = requests.post("http://api.epn.bz/json", data=json.dumps(data), headers=headers)

            deeplink = {
                "image": responce.json()["results"]["request_1"]["offer"]["picture"],
                "title": item[0],
                "url": responce.json()["results"]["request_1"]["offer"]["url"],
                "price": responce.json()["results"]["request_1"]["offer"]["sale_price"],
                "sale": int((responce.json()["results"]["request_1"]["offer"]["sale_price"] / responce.json()["results"]["request_1"]["offer"]["price"]) * 100),
                "group_id": self.group.id,
                "user_id": self.group.user_id
            }

            deeplinks.append(deeplink)

        return deeplinks
