import requests
import json
from BLL.Exeptions.EpnWrongAuthException import EpnWrongAuthException
from BLL.Exeptions.EpnOfferNotFoundException import EpnOfferNotFoundException
from BLL.Exeptions.EpnBadDeeplinkHashException import EpnBadDeeplinkHashException


class EPNService:

    def __init__(self, user, group):
        self.user = user
        self.group = group

    @staticmethod
    def __build_request_data(user, vk_items: list):

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
    def __send_request(user, vk_items: list):

        data = EPNService.__build_request_data(user, vk_items)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post("http://api.epn.bz/json",
                                 data=json.dumps(data),
                                 headers=headers)

        print(response.json())

        if "error" in response.json():
            if response.json()["error"] == 'Bad auth data!':
                raise EpnWrongAuthException("Wrong auth data!")
            elif response.json()["error"] == 'Bad deeplink hash!':
                raise EpnBadDeeplinkHashException("Bad deeplink hash!")

        return response.json()

    @staticmethod
    def __deeplink_customization(group_id, user_id, vk_items, response, counter):

        if "error" in response["results"]["rq_" + str(counter)]:
            print("error")
            if response["results"]["rq_" + str(counter)]["error"] == "Offer not found":
                raise EpnOfferNotFoundException("No such offer on Aliexpress!")

        sale = (response["results"]["rq_" + str(counter)]["offer"]["sale_price"] /
                response["results"]["rq_" + str(counter)]["offer"]["price"])

        if sale < 0.1:
            sale = int(sale * 10)
        elif sale >= 0.1:
            sale = int(sale * 100)

        deeplink = {
            "image": response["results"]["rq_" + str(counter)]["offer"]["picture"],
            "title": vk_items[counter][0],
            "url": response["results"]["rq_" + str(counter)]["offer"]["url"],
            "price": response["results"]["rq_" + str(counter)]["offer"]["sale_price"],
            "sale": sale,
            "group_id": group_id,
            "user_id": user_id
        }

        return deeplink

    def create_deeplinks(self, vk_items: list):

        response = EPNService.__send_request(self.user, vk_items)

        deeplinks = list()

        counter = 0
        for item in response["results"]:

            try:
                deeplinks.append(
                    EPNService.__deeplink_customization(self.group.id, self.group.user_id, vk_items, response,
                                                        counter))
            except EpnOfferNotFoundException as e:
                print(e.message + "for user" + self.group.user_id)
            except Exception as e:
                print("EPNService.create_deeplinks error")

            counter = + 1

        return deeplinks
