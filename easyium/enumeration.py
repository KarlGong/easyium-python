class WebDriverType:
    IE = "ie"
    FIREFOX = "firefox"
    CHROME = "chrome"
    OPERA = "opera"
    SAFARI = "safari"
    EDGE = "edge"
    PHANTOMJS = "phantomjs"
    ANDROID = "android"
    IOS = "ios"

    _BROWSER = [IE, FIREFOX, CHROME, OPERA, SAFARI, PHANTOMJS]
    _MOBILE = [ANDROID, IOS]
    _ALL = _BROWSER + _MOBILE
