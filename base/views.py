from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def index(request):     # home page view
    return render(request, 'base/index.html')


@require_http_methods(["POST"])
def change_language(request):  # change language drop list
    response = HttpResponseRedirect('/')
    language = request.POST.get('language')

    if not language:
        return response

    if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
        redirect_path = f'/{language}/'
    elif language == settings.LANGUAGE_CODE:
        redirect_path = '/'
    else:
        return response

    from django.utils import translation
    translation.activate(language)
    response = HttpResponseRedirect(redirect_path)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    return response

