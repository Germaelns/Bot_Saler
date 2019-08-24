import telebot
from telebot import types


class TGService:

    def __init__(self, user, bot):
        self.user = user
        self.bot = bot

    def post_to_channel(self, post_data):
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Заказать', url=post_data["url"])
        markup.add(btn_my_site)

        self.bot.send_photo(chat_id=self.user.tg_channel, photo=post_data["image"],
                            caption=f"\n {post_data['title']}\n\n"
                                    f"Цена: {post_data['price']}\n"
                                    f"Скидка: {str(post_data['sale'])}%",
                            reply_markup=markup)

        return 0
