from uuid import uuid4

from flask import Flask, request, abort, render_template, flash, redirect
from redis import StrictRedis

from parser import parse

app = Flask(__name__)
app.config.from_object('config')

redis = StrictRedis.from_url(app.config['REDIS_URL'])


def get_key(list_id):
    return 'jukephone:' + list_id


def make_song_response(song):
    if song is None:
        return abort(404)
    if song == 'null':
        return '', 204, {'Content-Type': 'text/plain'}
    return song, 200, {'Content-Type': 'text/plain'}


@app.route('/', methods=['GET'])
def health_check():
    if redis.ping():
        return '', 204
    else:
        abort(500)


@app.route('/', methods=['POST'])
def create_list():
    list_id = str(uuid4())
    key = get_key(list_id)

    redis.lpush(key, 'null')

    if request.base_url.endswith('/'):
        location = request.base_url + list_id
    else:
        location = request.base_uri + '/' + list_id

    return '', 201, {'Location': location}


@app.route('/<uuid:list_id>', methods=['GET'])
def get_current_song(list_id):
    list_id = str(list_id)
    key = get_key(list_id)

    song = redis.lindex(key, -1)
    return make_song_response(song)


@app.route('/<uuid:list_id>/next', methods=['POST'])
def next_song(list_id):
    list_id = str(list_id)
    key = get_key(list_id)

    songs_count = redis.llen(key)
    if songs_count == 0:  # No such list
        return abort(404)
    if songs_count == 1:  # Last song
        redis.lpush(key, 'null')

    redis.rpop(key)

    song = redis.lindex(key, -1)
    return make_song_response(song)


@app.route('/<uuid:list_id>.html', methods=['GET'])
def add_song_page(list_id):
    list_id = str(list_id)
    key = get_key(list_id)

    if not redis.exists(key):
        return abort(404)

    return render_template('jukephone.html')


@app.route('/<uuid:list_id>.html', methods=['POST'])
def add_song(list_id):
    list_id = str(list_id)
    key = get_key(list_id)

    if not redis.exists(key):
        return abort(404)

    try:
        song = parse(request.form['song'])
        redis.lpush(key, song)
    except Exception, ex:
        app.logger.warn(ex)
        flash('Failed to add the song :(', category='danger')
    else:
        flash('Your song is added successfully :)', category='success')

    return redirect(request.url)
