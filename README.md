# Jukephone Server
Server of Jukephone

## API

### `GET /`

Health check

- 204
- 500

### `POST /`

Create song list

- 201 with `Location: /:id` header

### `GET /:id`

Get current song

- 200 with `url` body
- 404

### `POST /:id/next`

Get next song

- 200 with `url` body
- 404

### `GET /:id.html`

Get add song web page

- 200 with a page
- 404

### `POST /:id.html`

Add song with `url=` body

- 302 with `Location: /:id.html` header
- 404
