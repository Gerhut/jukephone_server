from urlparse import urlsplit
from uuid import uuid4

import pytest
from redis import StrictRedis

from app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


@pytest.fixture
def redis():
    redis = StrictRedis.from_url(app.config['REDIS_URL'])
    redis.flushdb()
    yield redis


def test_health_check(client):
    assert client.get('/').status_code == 204


def test_create_list(client, redis):
    rv = client.post('/')
    assert rv.status_code == 201
    assert 'Location' in rv.headers

    list_id = urlsplit(rv.headers['Location']).path.lstrip('/')
    assert redis.exists('jukephone:' + list_id)


def test_get_current_song(client, redis):
    list_id = uuid4()

    rv = client.get('/' + str(list_id))
    assert rv.status_code == 404

    redis.lpush('jukephone:' + str(list_id), 'foo.mp3')
    redis.lpush('jukephone:' + str(list_id), 'bar.mp3')

    rv = client.get('/' + str(list_id))
    assert rv.status_code == 200
    assert rv.data == 'foo.mp3'


def test_next_song(client, redis):
    list_id = uuid4()

    rv = client.post('/' + str(list_id) + '/next')
    assert rv.status_code == 404

    redis.lpush('jukephone:' + str(list_id), 'foo.mp3')
    redis.lpush('jukephone:' + str(list_id), 'bar.mp3')

    rv = client.post('/' + str(list_id) + '/next')
    assert rv.status_code == 200
    assert rv.data == 'bar.mp3'

    rv = client.post('/' + str(list_id) + '/next')
    assert rv.status_code == 204

    rv = client.post('/' + str(list_id) + '/next')
    assert rv.status_code == 204


def test_add_song_page(client, redis):
    list_id = uuid4()

    rv = client.get('/' + str(list_id) + '.html')
    assert rv.status_code == 404

    redis.lpush('jukephone:' + str(list_id), 'null')

    rv = client.get('/' + str(list_id) + '.html')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/html'


def test_add_song(client, redis):
    list_id = uuid4()

    rv = client.post('/' + str(list_id) + '.html')
    assert rv.status_code == 404

    redis.lpush('jukephone:' + str(list_id), 'null')

    rv = client.post('/' + str(list_id) + '.html',
                     data={"song": "http://example.com/foo.mp3"},
                     follow_redirects=True)
    assert ':)' in rv.data
    assert redis.llen('jukephone:' + str(list_id)) == 2
    assert redis.lindex('jukephone:' + str(list_id), 0) == 'http://example.com/foo.mp3'

    rv = client.post('/' + str(list_id) + '.html',
                     data={"song": "foo.mp3"},
                     follow_redirects=True)
    assert ':(' in rv.data
    assert redis.llen('jukephone:' + str(list_id)) == 2
