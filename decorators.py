from flask import g, request, abort
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(self, **kwargs):
        x_authenticated_as = request.headers.get('X-Authenticated-As')
        if x_authenticated_as is None:
            abort(401, "please authenticate correctly using X-Authenticated-As HTTP header")
        g.logged_user = x_authenticated_as
        return view(self, **kwargs)
    return wrapped_view



