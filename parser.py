from posixpath import splitext
from urlparse import urlsplit

from zhuaxia.option import Option
from zhuaxia.xiami import Xiami, XiamiSong
from zhuaxia.netease import Netease, NeteaseSong

__all__ = ['parse']

option = Option()
xiami = Xiami(None, None, option)
netease = Netease(option)


def parse(url):
    '''
    Try parse a Xiami / Netease music page to audio url.
    '''

    (scheme, netloc, path, query, fragment) = urlsplit(url)
    if not scheme or not netloc or not path:
        raise ValueError('Invalid URL: ' + url)

    (root, extension) = splitext(path)
    if extension == '.mp3':
        return url

    if netloc == 'www.xiami.com':
        xiami_song = XiamiSong(xiami, url)
        return xiami_song.dl_link
    if netloc == 'music.163.com':
        netease_song = NeteaseSong(netease, url)
        return netease_song.dl_link

    raise ValueError('Cannot parse URL: ' + url)
