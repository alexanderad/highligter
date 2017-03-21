import httplib
import requests

from .. import app, request


def translate_text(text):
    key = 'translated:text:{}'.format(text)
    translated = app.redis.get(key)
    if translated:
        return {'success': True, 'text': translated, 'cache': 'hit'}

    url = (
        'https://translate.yandex.net/api/v1.5/tr.json/translate?'
        'key={}&lang=ro-en&text={}'
    )
    response = requests.get(
        url.format(app.config['yandex.api_key'], text)).json()

    if response.get('code') == httplib.OK:
        translated = response.get('text').pop()
    else:
        return {'success': False, 'error': response}

    app.redis.incr('translated:count')
    app.redis.incrby('translated:count_characters', len(text))
    app.redis.setnx('translated:text:{}'.format(text), translated)

    return {'success': True, 'text': translated, 'cache': 'miss'}


@app.route('/v1/translate')
def translate():
    text = request.params.get('text')
    if text is None:
        return {'success': False, 'error': 'no text given'}

    if len(text) > 128:
        return {'success': False, 'error': 'text is too long'}

    return translate_text(text)
