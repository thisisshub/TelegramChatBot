from db import DB
import json, requests, time, urllib

TOKEN = "2147462221:AAGzN2XbviUM8D2V6dha-r6dI9TrQ0VZXLI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    """Downloads the content from a URL and returns a string"""
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    """Gets the string response as above and parses this into a python dictionary"""
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    """Retrieves a list of messages sent to our bot"""
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    """Get the chat ID and the message text of the most recent message sent to our bot"""
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

db = DB()

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)  ##
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text in items:
            db.delete_item(text, chat)  ##
            items = db.get_items(chat)  ##
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        else:
            db.add_item(text, chat)  ##
            items = db.get_items(chat)  ##
            message = "\n".join(items)
            send_message(message, chat)


def get_last_update_id(updates):
    """Calculates the highest ID of all the updates we receive from getUpdates"""
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)



if __name__ == '__main__':
    main()