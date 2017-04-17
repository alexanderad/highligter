from .. import app, template, request, redirect


@app.route('/')
def index():
    app.redis.inc('counters:index:views')

    return template('index')


@app.route('/parse')
def parse():
    app.redis.inc('counters:parse:views')

    url = request.params.get('u')
    if not url:
        return redirect('/')

    return template('parse')


@app.route('/read')
def read():
    app.redis.inc('counters:read:views')

    page_id = request.params.get('t')
    if not page_id:
        return redirect('/')

    root_key = 'pages:{}'.format(page_id)
    url = app.redis.get(root_key)
    if not url:
        return redirect('/')

    app.redis.inc('{}:views'.format(root_key))
    page = {
        key: app.redis.get('{}:{}'.format(root_key, key))
        for key in ('title', 'domain', 'content', 'next_page_url')
    }

    return template('read', url=url, **page)
