# Define Configuration as an object
# This keeps the VIEWS file a little cleaner (hopefully)
import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'XSBseLG$e3b5aa4fcb163c87242a'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/cms.db' % os.getcwd()
    POSTS_PER_PAGE = 5
