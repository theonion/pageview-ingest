import os
import random
import time

hosts = (
    "www.theonion.com",
    "www.avclub.com",
    "www.clickhole.com",
    "www.onionstudios.com",
    "www.starwipe.com",
    "onion.local",
    "avclub.local",
    "clickhole.local",
    "videohub.local",
    "starwipe.local",
    "test.theonion.com",
    "test.avclub.com",
    "test.clickhole.com",
    "test.onionstudios.com",
    "master.test.starwipe.com",
    "staff.theonion.com",
    "staff.avclub.com",
    "staff.clickhole.com",
    "cms.onionstudios.com",
    "staff.starwipe.com",
    "www.gizzoogle.com",
)

paths = (
    "/article/blah-123",
    "/video/blah-123",
    "/special/travel/",
    "/series/mothershould",
    "/",
)

while 1:
    template = 'curl "http://10.0.2.15/ingest.gif?hostname={}&pathname={}"'
    host = random.choice(hosts)
    path = random.choice(paths)
    cmd = template.format(host, path)
    os.system(cmd)
    sleep = random.randrange(100) / 1000.0
    time.sleep(sleep)
