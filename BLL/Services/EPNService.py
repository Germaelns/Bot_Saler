import requests
import json


class EPNService:

    def __init__(self, user, group):
        self.user = user
        self.group = group

    @staticmethod
    def build_request_data(user, vk_items: list):

        data = {
            "user_api_key": "" + user.epn_api_token,
            "user_hash": "" + user.epn_hash,
            "api_version": 1,
            "requests": {

            }
        }

        counter = 0

        for item in vk_items:
            data["requests"]["rq_" + str(counter)] = {
                "action": "offer_info",
                "lang": "ru",
                "id": "" + item[1],
                "currency": "USD"

            }

            counter = + 1

        return data

    @staticmethod
    def send_request(user, vk_items):

        data = EPNService.build_request_data(user, vk_items)
        headers = {
            'Content-Type': 'application/json'
        }

        return requests.post("http://api.epn.bz/json", data=json.dumps(data), headers=headers)

    def create_deeplinks(self, vk_items: list):

        responce = EPNService.send_request(self.user, vk_items)

        deeplinks = list()

        counter = 0
        for item in responce.json()["results"]:

            deeplink = {
                "image": responce.json()["results"]["rq_" + str(counter)]["offer"]["picture"],
                "title": vk_items[counter][0],
                "url": responce.json()["results"]["rq_" + str(counter)]["offer"]["url"],
                "price": responce.json()["results"]["rq_" + str(counter)]["offer"]["sale_price"],
                "sale": int((responce.json()["results"]["rq_" + str(counter)]["offer"]["sale_price"] / responce.json()["results"]["rq_" + str(counter)]["offer"]["price"]) * 100),
                "group_id": self.group.id,
                "user_id": self.group.user_id
            }

            deeplinks.append(deeplink)
            counter = + 1

        return deeplinks
