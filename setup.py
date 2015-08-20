from setuptools import setup

setup(
    name="pageview_ingest",
    version="0.0.1",

    packages=["pageview_ingest", ],
    install_requires=["gevent==1.0.2", "psycopg2==2.6.1", "pytz==2015.4", ],

    author="Vince Forgione",
    author_email="vforgione@theonion.com",
    description="A simple, fast uwsgi/gevent application to record pageview data to Postgres",
    license="MIT",
    keywords=["uwsgi gevent postgres pageview"],
    url="https://github.com/theonion/pageview-ingest",
)
