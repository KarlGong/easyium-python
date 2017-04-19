class WebDriverType:
    IE = "ie"
    FIREFOX = "firefox"
    CHROME = "chrome"
    OPERA = "opera"
    SAFARI = "safari"
    EDGE = "edge"
    PHANTOMJS = "phantomjs"
    REMOTE = "remote"
    ANDROID = "android"
    IOS = "ios"

    _BROWSER = [IE, FIREFOX, CHROME, OPERA, SAFARI, EDGE, PHANTOMJS, REMOTE]
    _MOBILE = [ANDROID, IOS]
    _ALL = _BROWSER + _MOBILE
