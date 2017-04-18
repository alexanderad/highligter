import requests

from app import app, request
from app.misc import hashies
from app.misc.vacuum import Vacuum


@app.route('/v1/parse', method='POST')
def parse():
    url = request.params.get('url').strip()
    if not url:
        return {'success': False, 'error': 'no url given'}

    url_hash = hashies.md5(url)
    key = 'pages:{}:page_id'.format(url_hash)
    page_id = app.redis.get(key)
    if page_id:
        return {'success': True, 'page_id': page_id, 'cache': 'hit'}

    data = requests.get(
        app.config['mercury.parser_endpoint'],
        params=dict(url=url),
        headers={'x-api-key': app.config['mercury.api_key']}
    ).json()

    if data.get('error'):
        return {'success': False, 'error': data['messages']}

    page_id = hashies.short_id()
    content = Vacuum(
        data.get('content'),
        salt=app.config['app.secret'],
        https_proxy=app.config['app.https_proxy']
    ).apply_all()

    # counters
    app.redis.incr('counters:requests:parse')

    # data
    app.redis.set(key, page_id)
    app.redis.lpush('pages:recent', page_id)
    app.redis.set('pages:{}'.format(page_id), url)
    app.redis.set('pages:{}:title'.format(page_id), data.get('title'))
    app.redis.set('pages:{}:content'.format(page_id), content)
    app.redis.set('pages:{}:image'.format(page_id), data.get('lead_image_url'))
    app.redis.set('pages:{}:domain'.format(page_id), data.get('domain'))
    app.redis.set(
        'pages:{}:next_page_url'.format(page_id), data.get('next_page_url'))

    return {'success': True, 'page_id': page_id, 'cache': 'miss'}