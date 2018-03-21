import asyncio
import logging
import os
import voluptuous as vol
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import socket

DOMAIN = 'movie'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({}),
}, extra=vol.ALLOW_EXTRA)

movie = {}
movie_name = []


def get_movie_data():
    url = "https://api.douban.com/v2/movie/in_theaters"
    api_key = "0b2bdeda43b5688921839c8ecb20399b"
    city = "北京"
    params = {"city": city, "apikey": api_key}
    r = requests.get(url, params)
    content = r.json()
    for i in range(10):
        movie_name.append("-" + content["subjects"][i]["title"])
        movie["-" + content["subjects"][i]["title"]] = "- " + content["subjects"][i]["title"] + " " + \
                                                       content["subjects"][i]["genres"][0] + " " + \
                                                       content["subjects"][i]["durations"][0] + " " + \
                                                       str(content["subjects"][i]["collect_count"]) + "人看过 " + \
                                                       "大陆上映时间:" + str(
            content["subjects"][i]["mainland_pubdate"] + "\n ")


def restart_ha():
    import platform
    os_name = platform.platform()[:7]
    if os_name.upper() == "WINDOWS":
        os.system("curl -d \"\" http://" + get_host_ip() + ":8123/api/services/homeassistant/restart")
    else:
        os.system("sudo systemctl restart home-assistant@homeassistant.service")


def get_host_ip():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


@asyncio.coroutine
def async_setup(hass):
    """Set up the movie component."""
    scheduler = BlockingScheduler()
    scheduler.add_job(restart_ha, 'cron', day_of_week='0-6', hour=2, minute=00)
    scheduler.start()
    log = logging.getLogger(__name__)
    log.info("Running")
    get_movie_data()
    # print(movie)
    con = ""
    for name in range(len(movie_name)):
        con = con + movie[movie_name[name]] + "\n"

    hass.components.persistent_notification.async_create(
        con, "最近上映的电影")

    return True
