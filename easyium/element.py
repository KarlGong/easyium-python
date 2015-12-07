from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from .config import DEFAULT
from .context import Context
from .decorator import SupportedBy
from .exceptions import EasyiumException, NoSuchElementException
from .waiter import ElementWaitFor
from .webdriver import WebDriverType

__author__ = 'karl.gong'


class Element(Context):
    def __init__(self, parent):
        Context.__init__(self)
        self.__parent = parent

    def get_web_driver(self):
        return self.get_parent().get_web_driver()

    get_browser = get_web_driver

    def get_web_driver_type(self):
        return self.get_web_driver().get_web_driver_type()

    get_browser_type = get_web_driver_type

    def get_wait_interval(self):
        return self.get_web_driver().get_wait_interval()

    def get_wait_timeout(self):
        return self.get_web_driver().get_wait_timeout()

    def get_pre_wait_time(self):
        return self.get_web_driver().get_pre_wait_time()

    def get_post_wait_time(self):
        return self.get_web_driver().get_post_wait_time()

    def get_parent(self):
        return self.__parent

    def _selenium_element(self):
        pass

    def wait_for(self, interval=DEFAULT, timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT):
        """
            Get a ElementWaitFor instance.

        :param interval: the wait interval (in milliseconds), default value is web driver's wait interval
        :param timeout: the wait timeout (in milliseconds), default value is web driver's wait timeout
        :param pre_wait_time: the pre wait time (in milliseconds), default value is web driver's pre wait time
        :param post_wait_time: the post wait time (in milliseconds), default value is web driver's post wait time
        """
        _interval = self.get_wait_interval() if interval == DEFAULT else interval
        _timeout = self.get_wait_timeout() if timeout == DEFAULT else timeout
        _pre_wait_time = self.get_pre_wait_time() if pre_wait_time == DEFAULT else pre_wait_time
        _post_wait_time = self.get_post_wait_time() if post_wait_time == DEFAULT else post_wait_time
        return ElementWaitFor(self, _interval, _timeout, _pre_wait_time, _post_wait_time)

    def blur(self):
        try:
            try:
                self.get_web_driver().execute_script("arguments[0].blur()", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().execute_script("arguments[0].blur()", self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def clear(self):
        try:
            try:
                self._selenium_element().clear()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().clear()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def click(self):
        try:
            try:
                self._selenium_element().click()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().click()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def double_click(self):
        try:
            try:
                self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def context_click(self):
        try:
            try:
                self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def send_keys(self, value):
        try:
            try:
                self._selenium_element().send_keys(value)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().send_keys(value)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def submit(self):
        try:
            try:
                self._selenium_element().submit()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().submit()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_attribute(self, name):
        try:
            try:
                return self._selenium_element().get_attribute(name)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute(name)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_css_value(self, property_name):
        try:
            try:
                return self._selenium_element().value_of_css_property(property_name)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().value_of_css_property(property_name)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_location(self):
        """
            Gets the location for the top-left corner of this element.

        :Usage:
            x, y = element.get_location()
        """
        try:
            try:
                location = self._selenium_element().location
                return location["x"], location["y"]
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                location = self._selenium_element().location
                return location["x"], location["y"]
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_size(self):
        """
            Gets the size (including border) of this element.

        :Usage:
            width, height = element.get_size()
        """
        try:
            try:
                size = self._selenium_element().size
                return size["width"], size["height"]
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                size = self._selenium_element().size
                return size["width"], size["height"]
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_tag_name(self):
        try:
            try:
                return self._selenium_element().tag_name
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().tag_name
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_value(self):
        try:
            try:
                return self._selenium_element().get_attribute("value")
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute("value")
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_text(self):
        try:
            try:
                return self._selenium_element().text
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().text
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_text_node_content(self, text_node_index):
        """
            Get content of the text node in this element.
            If the text_node_index refers to a non-text node or be out of bounds, an exception will be thrown.

        :param text_node_index: index of text node in this element
        :return: the content of the text node in this element.
        """
        try:
            try:
                content = self.get_web_driver().execute_script(
                    "return arguments[0].childNodes[%s].nodeValue" % text_node_index, self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                content = self.get_web_driver().execute_script(
                    "return arguments[0].childNodes[%s].nodeValue" % text_node_index, self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

        if content is None:
            raise EasyiumException("Cannot get text content of a non-text node in element: \n%s\n" % self)
        return content

    def set_selection_range(self, start, end):
        """
            Set the selection range for text in this element.

        :param start: start position
        :param end: end position
        """
        script = """
            function getTextNodesIn(node) {
                var textNodes = [];
                if (node.nodeType == 3) {
                    textNodes.push(node);
                } else {
                    var children = node.childNodes;
                    for (var i = 0, len = children.length; i < len; ++i) {
                        textNodes.push.apply(textNodes, getTextNodesIn(children[i]));
                    }
                }
                return textNodes;
            }

            function setSelectionRange(el, start, end) {
                if (el.tagName == 'INPUT' || el.tagName == 'TEXTAREA'){
                    if(el.createTextRange){
                        var Range=el.createTextRange();
                        Range.collapse();
                        Range.moveEnd('character',end);
                        Range.moveStart('character',start);
                        Range.select();
                    }else if(el.setSelectionRange){
                        el.focus();
                        el.setSelectionRange(start,end);
                    }
                } else {
					if (document.createRange && window.getSelection) {
                        var range = document.createRange();
                        range.selectNodeContents(el);
                        var textNodes = getTextNodesIn(el);
                        var foundStart = false;
                        var charCount = 0, endCharCount;

                        for (var i = 0, textNode; textNode = textNodes[i++]; ) {
                            endCharCount = charCount + textNode.length;
                            if (!foundStart && start >= charCount
                                    && (start < endCharCount ||
                                    (start == endCharCount && i < textNodes.length))) {
                                range.setStart(textNode, start - charCount);
                                foundStart = true;
                            }
                            if (foundStart && end <= endCharCount) {
                                range.setEnd(textNode, end - charCount);
                                break;
                            }
                            charCount = endCharCount;
                        }

                        var sel = window.getSelection();
                        sel.removeAllRanges();
                        sel.addRange(range);
                    } else if (document.selection && document.body.createTextRange) {
                        var textRange = document.body.createTextRange();
                        textRange.moveToElementText(el);
                        textRange.collapse(true);
                        textRange.moveEnd('character', end);
                        textRange.moveStart('character', start);
                        textRange.select();
                    }
				}
            }

            setSelectionRange(arguments[0], %s, %s);
        """
        try:
            try:
                self.get_web_driver().execute_script(script % (start, end), self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().execute_script(script % (start, end), self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def get_inner_html(self):
        try:
            try:
                return self.get_web_driver().execute_script("return arguments[0].innerHTML", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self.get_web_driver().execute_script("return arguments[0].innerHTML", self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def is_enabled(self):
        try:
            try:
                return self._selenium_element().is_enabled()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_enabled()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def is_selected(self):
        try:
            try:
                return self._selenium_element().is_selected()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_selected()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._BROWSER)
    def mouse_over(self):
        script = """
            var evObj = document.createEvent('MouseEvents');
            evObj.initMouseEvent("mouseover", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            arguments[0].dispatchEvent(evObj);
        """
        try:
            try:
                self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self.get_web_driver().execute_script(script, self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._BROWSER)
    def mouse_out(self):
        script = """
            var evObj = document.createEvent('MouseEvents');
            evObj.initMouseEvent("mouseout", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            arguments[0].dispatchEvent(evObj);
        """
        try:
            try:
                self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self.get_web_driver().execute_script(script, self)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._BROWSER)
    def drag_and_drop_by_offset(self, x_offset, y_offset):
        """
            Drag and drop to target offset.

        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        try:
            try:
                self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(x_offset, y_offset).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(x_offset, y_offset).release().perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def drag_and_drop_to(self, target_element):
        """
            Drag and drop to target element.

        :param target_element: the target element to drop
        """
        web_driver_type = self.get_web_driver_type()
        try:
            try:
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element()).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(
                        self._selenium_element()).move_to_element(self._selenium_element()).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element()).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(
                        self._selenium_element()).move_to_element(self._selenium_element()).release().perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._BROWSER)
    def drag_and_drop_to_with_offset(self, target_element, x_offset, y_offset):
        """
            Drag and drop to target element with offset.
            The origin is at the top-left corner of web driver and offsets are relative to the top-left corner of the element.

        :param target_element: the target element to drop
        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        try:
            try:
                self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                    self._selenium_element(), x_offset, y_offset).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                    self._selenium_element(), x_offset, y_offset).release().perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def tap(self, count=1):
        try:
            try:
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def long_press(self, duration=1000):
        try:
            try:
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType.ANDROID)
    def set_text(self, text):
        """
            Sends text to this element. Previous text is removed.
            Android only.

        :param text: the text to be sent to this element
        """
        try:
            try:
                self._selenium_element().set_text(text)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self._selenium_element().set_text(text)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def get_location_in_view(self):
        """
            Gets the location of an element relative to the view.

        :Usage:
            x, y = element.get_location_in_view()
        """
        try:
            try:
                location = self._selenium_element().location_in_view
                return location["x"], location["y"]
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                location = self._selenium_element().location_in_view
                return location["x"], location["y"]
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def set_value(self, value):
        """
            Set the value on this element in the application

        :param value: the value to be set on this element
        """
        try:
            try:
                self._selenium_element().set_value(value)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self._selenium_element().set_value(value)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def scroll_to(self, target_element):
        """
            Scrolls from this element to another.

        :param target_element: the target element to be scrolled to
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().scroll(self._selenium_element(),
                                                                    target_element._selenium_element())
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                target_element.wait_for().exists()
                self.get_web_driver()._selenium_web_driver().scroll(self._selenium_element(),
                                                                    target_element._selenium_element())
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def pinch(self, percent=200, steps=50):
        """
            Pinch on this element a certain amount

        :param percent: amount to pinch. Defaults to 200%
        :param steps: number of steps in the pinch action
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().pinch(self._selenium_element(), percent, steps)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver()._selenium_web_driver().pinch(self._selenium_element(), percent, steps)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    @SupportedBy(WebDriverType._MOBILE)
    def zoom(self, percent=200, steps=50):
        """
            Zooms in on an element a certain amount.

        :param percent: amount to zoom. Defaults to 200%
        :param steps: number of steps in the zoom action
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().zoom(self._selenium_element(), percent, steps)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver()._selenium_web_driver().zoom(self._selenium_element(), percent, steps)
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def is_displayed(self):
        try:
            try:
                return self._selenium_element().is_displayed()
            except StaleElementReferenceException:
                self._refresh()
                return self._selenium_element().is_displayed()
        except NoSuchElementException:
            return False
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))

    def exists(self):
        try:
            try:
                self._selenium_element().is_displayed()
                return True
            except StaleElementReferenceException:
                self._refresh()
                return True
        except NoSuchElementException:
            return False
        except WebDriverException as wde:
            raise EasyiumException("%s\n%s" % (wde.msg, self))
