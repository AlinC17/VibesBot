import re

def get_user_id(url):
    pattern = re.compile('[0-9]+')
    return pattern.search(url).group(0)

def get_album_id(url):
    pattern = re.compile('_[0-9]+')
    url_done = pattern.search(url).group(0)
    return url_done.replace('_', '')

def get_artist_title(name):
    pattern = re.compile('[0-9]+')
    return pattern.search().group(0)