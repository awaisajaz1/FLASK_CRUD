from functools import wraps
from flask import request, redirect, current_app


SECONDS_PER_YEAR = int(60*60*24*365)


def redirect_to_https(status_code=302):
    """ Redirect a request to https.
    """
    criteria = [
        request.is_secure,
        request.headers.get('X-Forwarded-Proto', 'http') == 'https'
    ]
    if not any(criteria):
        if request.url.startswith('http://'):
            new_url = request.url.replace("http://", "https://", 1)
            return redirect(new_url, code=status_code)


def default_hsts_header(max_age=SECONDS_PER_YEAR):
    """ Returns the default HSTS policy.
    """
    return 'max-age={0}'.format(max_age)


def set_hsts_header(response):
    """ Adds HSTS header to each response.
    """
    if request.is_secure:
        response.headers.setdefault(
            'Strict-Transport-Security', default_hsts_header())
    return response


class RequireHTTPS(object):
    """ Makes https required for a Flask app.
    """
    def __init__(self, app=None):
        self.app = app or current_app
        if app is not None:
            self.enable_https_requirement(app)

    def enable_https_requirement(self, app):
        app.before_request(redirect_to_https)
        app.after_request(set_hsts_header)
