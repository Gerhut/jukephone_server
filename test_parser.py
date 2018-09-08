from parser import parse


def test_parse_mp3():
    url = 'http://m10.music.126.net/20180908172249/3fa75b1b63ae8e55036de9e623c4a6e5/ymusic/90a0/2704/8287/6221353e3ecfceb957aa8fd526a85812.mp3'
    assert parse(url) == url


def test_parse_xiami():
    url = 'https://www.xiami.com/song/1796413084'
    audio_url = parse(url)
    assert parse(audio_url) == audio_url


def test_parse_netease():
    url = 'https://music.163.com/#/song?id=27896132'
    audio_url = parse(url)
    assert parse(audio_url) == audio_url
