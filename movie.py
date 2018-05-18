import asyncio
import logging
import os
import socket

import voluptuous as vol
import requests

REQUIREMENTS = ['apscheduler']
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
    os.system("curl -d \"\" http://" + get_host_ip() + ":8123/api/services/homeassistant/restart")


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
def async_setup(hass, config=None):
    """Set up the movie component."""

    log = logging.getLogger(__name__)
    log.info("Running")
    get_movie_data()
    # print(movie)
    con = ""
    for name in range(len(movie_name)):
        con = con + movie[movie_name[name]] + "\n"

    hass.components.persistent_notification.async_create(
        con, "最近上映的电影")
    start_job()
    return True


def start_job():
    """
    minute： 表示分钟，可以是从0到59之间的任何整数。

    hour：表示小时，可以是从0到23之间的任何整数。

    day：表示日期，可以是从1到31之间的任何整数。

    month：表示月份，可以是从1到12之间的任何整数。

    week：表示星期几，可以是从0到7之间的任何整数，这里的0或7代表星期日。

    星号（*）：代表所有可能的值，例如month字段如果是星号，则表示在满足其它字段的制约条件后每月都执行该命令操作。

    逗号（,）：可以用逗号隔开的值指定一个列表范围，例如，“1,2,5,7,8,9”

    中杠（-）：可以用整数之间的中杠表示一个整数范围，例如“2-6”表示“2,3,4,5,6”

    正斜线（/）：可以用正斜线指定时间的间隔频率，例如“0-23/2”表示每两小时执行一次。同时正斜线可以和星号一起使用，例如*/10，
    如果用在minute字段，表示每十分钟执行一次。

    :return:
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart_ha, 'cron', day_of_week='0', hour=8, minute=00)
    scheduler.start()
