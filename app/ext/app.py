import os
import bottle
from bottle import Bottle, Router, Route, request

from beaker.session import Session, SessionObject
from beaker.util import coerce_session_params


class RouterExt(Router):
    """Extended router to address OPTIONS request at any route in order to
    serve pre-flight requests."""
    def match(self, environ):
        if request.method == 'OPTIONS':
            return Route(request.app, None, request.method, lambda: ''), {}
        return super(RouterExt, self).match(environ)


class BottleExt(Bottle):
    """There is no right way to do sessions in micro-framework (c)."""
    def __init__(self, *args, **kwargs):
        super(BottleExt, self).__init__(*args, **kwargs)
        self.router = RouterExt()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bottle.TEMPLATE_PATH = [os.path.join(dir_path, '..', 'templates/')]

    def setup_sessions(self, config):
        """Initialize the session."""
        # default options
        self.session_options = dict(
            invalidate_corrupt=True, type=None,
            data_dir=None, key='beaker.session.id',
            timeout=None, secret=None, log_file=None)

        # pull out any config args meant for beaker session
        for key, val in config.items():
            if key.startswith('session.'):
                self.session_options[key[8:]] = val

        # coerce and validate session params
        coerce_session_params(self.session_options)

    def add_cors_headers(self, headers):
        """Add CORS headers."""
        headers.append(('Access-Control-Allow-Origin',
                        request.app.config['app.access_control_allow_origin']))
        headers.append(('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE, OPTIONS'))
        headers.append(('Access-Control-Allow-Headers',
                        'Authorization, Content-Type, Accept'))
        headers.append(('Access-Control-Allow-Credentials', 'true'))

    def __call__(self, environ, start_response):
        session = SessionObject(environ, **self.session_options)

        environ['beaker.session'] = session
        environ['beaker.get_session'] = self._get_session

        def session_start_response(status, headers, exc_info=None):
            if session.accessed():
                session.persist()
                if session.__dict__['_headers']['set_cookie']:
                    cookie = session.__dict__['_headers']['cookie_out']
                    if cookie:
                        headers.append(('Set-cookie', cookie))

            self.add_cors_headers(headers)
            return start_response(status, headers, exc_info)

        return super(BottleExt, self).__call__(environ, session_start_response)

    def _get_session(self):
        return Session({}, use_cookies=False, **self.session_options)
