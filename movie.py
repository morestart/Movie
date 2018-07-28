import asyncio
import logging
from requests.exceptions import (
    ConnectionError as ConnectError, HTTPError, Timeout)
import requests
import voluptuous as vol


_LOGGER = logging.getLogger(__name__)
# REQUIREMENTS = ['apscheduler']
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
    try:
        for i in range(10):
            movie_name.append("-" + content["subjects"][i]["title"])
            movie["-" + content["subjects"][i]["title"]] = "- " + content["subjects"][i]["title"] + " " + \
                                                           content["subjects"][i]["genres"][0] + " " + \
                                                           content["subjects"][i]["durations"][0] + " " + \
                                                           str(content["subjects"][i]["collect_count"]) + "人看过 " + \
                                                           "大陆上映时间:" + str(
                content["subjects"][i]["mainland_pubdate"] + "\n ")
    except IndexError:
        for i in range(10):
            movie_name.append("-" + content["subjects"][i]["title"])
            movie["-" + content["subjects"][i]["title"]] = "- **" + content["subjects"][i]["title"] + "**" + " " + \
                                                           content["subjects"][i]["genres"][0] + " " + \
                                                           str(content["subjects"][i]["collect_count"]) + "人看过 " + \
                                                           "大陆上映时间:" + str(content["subjects"][i]["mainland_pubdate"])
    except (ConnectError, HTTPError, Timeout, ValueError) as error:
        _LOGGER.error("Unable to connect to HeWeather. %s", error)
        return


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

    return True
