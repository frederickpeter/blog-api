from django.conf import settings


def set_access_cookie(response, access_token, expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]):
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        value=access_token,
        expires=expires,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        path="/api",
    )
    return response


def set_refresh_cookie(response, refresh_token, expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]):
    response.set_cookie(
        key=settings.SIMPLE_JWT["REFRESH_COOKIE"],
        value=refresh_token,
        expires=expires,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    return response


def delete_access_and_refresh_cookie(response):
    response.delete_cookie(key=settings.SIMPLE_JWT["AUTH_COOKIE"])
    response.delete_cookie(key=settings.SIMPLE_JWT["REFRESH_COOKIE"])
    return response
