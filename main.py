import config
from pymongo import MongoClient
import telebot
import sys
# import os
import time
import datetime
# from PIL import Image, ImageDraw, ImageFont

bot = telebot.TeleBot(config.token)

# need to create class
MONGODB_URI = "mongodb://" + config.db_user + ":" + config.db_pass + "@ds123012.mlab.com:23012/zulbukharov_outlay"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("zulbukharov_outlay")
outlay = db.outlay



def push(data):
    return (outlay.insert(data))

def update(record, update):
    outlay.update_one({'_id': record['_id']}, {
        '$set': update
    }, upsert=False)

def find_one(user_id):
    return (outlay.find_one({"user_id": user_id}))

# finish of mongo

out = {
    "price": 0,
    "desc": "",
    "date": "",
    "time_sec": 0,
}

data = {
    "user_id": "",
    "outlay": [],
}

# @bot.message_handler(commands=['stat'])
# def make_stat(message):
#     print(outlay.count)
#     sum = 0;
#
#     img = Image.new('RGB', (250, 250), "black")  # create a new black image
#     pixels = img.load()  # create the pixel map
#
#     for i in range(img.size[0]):  # for every col:
#         for j in range(img.size[1]):  # For every row
#             pixels[i, j] = (i, j, 100)  # set the colour accordingly
#     fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
#     d = ImageDraw.Draw(img)
#
#     s = 10
#     for out in outlay.find():
#         d.text((10, s), out['desc'], font=fnt, fill=(255, 255, 0))
#         print(out)
#         s += 15
#         sum += out['price']
#     img.save(str(message.chat.username) + ".png")
#     bot.send_photo(message.chat.id, open(str(message.chat.username) + ".png", "rb"))
#     os.system("rm " + str(message.chat.id) + ".png")
#     bot.send_message(message.chat.id, sum)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print(message)
    m = message.text.split(" ")
    print(m)
    data["user_id"] = message.chat.id
    out["date"] = str(datetime.datetime.fromtimestamp(message.date))
    out["desc"] = ' '.join(m[1:])
    out["price"] = m[0]
    out["time_sec"] = int(message.date)
    res = find_one(message.chat.id)
    print(res)
    if not res:
        print('adding')
        data["outlay"].append(out)
        r = push(data)
        print(r)
    else:
        res["outlay"].append(out)
        print(res)
        update(res, res)
    bot.send_message(message.chat.id, "saved")

def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)