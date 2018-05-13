from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

EXEMPT_URLS = [settings.LOGIN_URL[1:-1]]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [url[1:-1] for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info

        # if not request.user.is_authenticated:
        #     if not any(path[1:-1] == url for url in EXEMPT_URLS):
        #         return redirect(settings.LOGIN_URL)

        # if path == reverse('accounts:logout'):
        #     logout(request)

        url_in_exempt = any(path[1:-1] == url for url in EXEMPT_URLS)

        if request.user.is_authenticated and url_in_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_in_exempt or path[0:33] == '/accounts/reset-password/confirm/':
            return None
        else:
            return redirect(settings.LOGIN_URL)
