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


def send_message(text, chat_id):
    """Sends the message to a particular chat id"""
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def echo_all(updates):
    """Send an echo reply for each message that we receive"""
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def main():
    last_textchat = (None, None)
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            send_message(text, chat)
            last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main()