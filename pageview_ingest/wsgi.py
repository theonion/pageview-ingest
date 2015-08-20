#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from collections import Counter
from datetime import datetime
import logging
import os
import sys

import gevent
from gevent.queue import Queue, Empty as QueueEmpty
import pytz
import psycopg2
import psycopg2.extras

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


gif = base64.b64decode("R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")

queue = Queue()

logger = logging.getLogger('ingest')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

timezone = pytz.timezone('America/Chicago')

flush_interval = 30  # seconds

valid_domains = ("theonion", "avclub", "clickhole", "onionstudios", "starwipe")

db_host = os.environ.get("INGEST_DB_HOST", "localhost")
db_port = os.environ.get("INGEST_DB_PORT", "5432")
db_user = os.environ.get("INGEST_DB_USER", "ingest")
db_passwd = os.environ.get("INGEST_DB_PASSWD", "ingest")
db_dbname = os.environ.get("INGEST_DB_DBNAME", "ingest")
connection = psycopg2.connect(database=db_dbname, user=db_user, password=db_passwd, host=db_host, port=db_port)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def aggregate():
    while 1:
        gevent.sleep(flush_interval)
        timestamp = get_timestamp()
        pageviews = Counter()
        trends = Counter()
        while 1:
            try:
                hostname, pathname, search = queue.get_nowait()
                host = get_host(hostname)
                if not host:
                    continue
                paths = pathname.split("-")
                last_path = paths[-1]
                if last_path.endswith("/"):
                    last_path = last_path[:-1]
                try:
                    content_id = int(last_path)
                except ValueError:
                    content_id = None
                if search:
                    pathname += search
                pageviews[(host, pathname)] += 1
                if content_id:
                    trends[(host, content_id)] += 1
            except QueueEmpty:
                break
            except Exception as e:
                logger.exception(e)
                break
        if len(pageviews):
            sys.stdout.write("working on {} pageviews\n".format(len(pageviews)))
            gevent.spawn(send_pageviews, pageviews, timestamp)
        if len(trends):
            sys.stdout.write("working on {} trends\n".format(len(trends)))
            gevent.spawn(send_trends, trends, timestamp)


gevent.spawn(aggregate)


def get_timestamp():
    naive_now = datetime.now()
    central_now = timezone.localize(naive_now)
    return central_now.strftime("%Y-%m-%d %H:%M:%S")


def get_host(hostname):
    parts = hostname.split(".")
    if len(parts) != 3:
            return None
    subdomain = parts[0]
    if subdomain != "www":
        return None
    domain = parts[1]
    if domain not in valid_domains:
        return None
    tld = parts[2]
    if tld != "com":
        return None
    return domain


def collate(counter):
    collated = {}
    for (host, key), count in counter.items():
        collated.setdefault(host, [])
        collated[host].append((key, count))
    return collated


def send_pageviews(pageviews, timestamp):
    site_pageviews = collate(pageviews)
    for site, pageviews in site_pageviews.items():
        values = []
        for (path, count) in pageviews:
            values.append({"path": path, "date": timestamp, "count": count})
        command = "INSERT INTO {}_pageviews(path, date, count) VALUES ".format(site)
        command += "(%(path)s, %(date)s, %(count)s);"
        try:
            res = cursor.executemany(command, values)
            sys.stdout.write("execute pageviews: {}\n".format(res))
        except Exception as e:
            logger.exception(e)


def send_trends(trends, timestamp):
    site_trends = collate(trends)
    for site, trends in site_trends.items():
        values = []
        for (content_id, count) in trends:
            values.append({"content_id": content_id, "date": timestamp, "count": count})
        command = "INSERT INTO {}_trends(content_id, date, count) VALUES ".format(site)
        command += "(%(content_id)s, %(date)s, %(count)s);"
        try:
            res = cursor.executemany(command, values)
            sys.stdout.write("execute trends: {}\n".format(res))
        except Exception as e:
            logger.exception(e)


def application(env, start_response):
    path = env["PATH_INFO"]
    if path == "/ingest.gif":
        start_response("200 OK", [("Content-Type", "image/gif")])
        yield gif
        try:
            params = parse_qs(env["QUERY_STRING"])
            hostname = params.get("hostname", [None])[0]
            pathname = params.get("pathname", [None])[0]
            search = params.get("search", [None])[0]
            if hostname and pathname:
                queue.put((hostname, pathname, search))
        except Exception as e:
            logger.exception(e)

    else:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        yield ""
