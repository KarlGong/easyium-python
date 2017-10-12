class WebDriverContext:
    IE = "ie"
    FIREFOX = "firefox"
    CHROME = "chrome"
    OPERA = "opera"
    SAFARI = "safari"
    EDGE = "edge"
    PHANTOMJS = "phantomjs"

    NATIVE_APP = "native_app"
    WEB_VIEW = "web_view"

    _WEB = [IE, FIREFOX, CHROME, OPERA, SAFARI, EDGE, PHANTOMJS, WEB_VIEW]
    _APP = [NATIVE_APP, WEB_VIEW]


class WebDriverPlatform:
    PC = "pc"
    ANDROID = "android"
    IOS = "ios"

    _MOBILE = [ANDROID, IOS]
