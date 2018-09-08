import logging
from datetime import timedelta
from requests.exceptions import (
    ConnectionError as ConnectError, HTTPError, Timeout)
import requests
from homeassistant.helpers import event


_LOGGER = logging.getLogger(__name__)
DOMAIN = 'movie'

movie = {}
movie_name = []


async def async_setup(hass, config):
    """Set up the movie component."""

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
                movie["-" + content["subjects"][i]["title"]] = "- **" + content["subjects"][i]["title"] + "**" + " " + \
                                                               content["subjects"][i]["genres"][0] + " " + \
                                                               content["subjects"][i]["durations"][0] + " " + \
                                                               str(content["subjects"][i]["collect_count"]) + "人看过 " + \
                                                               "大陆上映时间:" + str(
                    content["subjects"][i]["mainland_pubdate"] + "\n ")
            con = ""
            for name in range(len(movie_name)):
                con = con + movie[movie_name[name]] + "\n"
            movie.clear()
            movie_name.clear()
            return con
        except IndexError:
            for i in range(10):
                movie_name.append("-" + content["subjects"][i]["title"])
                movie["-" + content["subjects"][i]["title"]] = "- **" + content["subjects"][i]["title"] + "**" + " " + \
                                                               content["subjects"][i]["genres"][0] + " " + \
                                                               str(content["subjects"][i]["collect_count"]) + "人看过 " + \
                                                               "大陆上映时间:" + str(
                    content["subjects"][i]["mainland_pubdate"])
            con = ""
            for name in range(len(movie_name)):
                con = con + movie[movie_name[name]] + "\n"
            logging.error("Index" + con)
            return con
        except (ConnectError, HTTPError, Timeout, ValueError) as error:
            _LOGGER.error("Unable to connect to DouBan. %s", error)
            return error

    def creat_notification(event_time):
        hass.components.persistent_notification.async_create(
            get_movie_data(), "最近上映的电影")
    TIME_BETWEEN_UPDATES = timedelta(minutes=1)

    event.async_track_time_interval(
        hass, creat_notification, TIME_BETWEEN_UPDATES)

    return True
