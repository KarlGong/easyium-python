from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, ElementNotVisibleException

from .context import Context
from .decorator import SupportedBy
from .exceptions import EasyiumException, NoSuchElementException
from .waiter import ElementWaitFor
from .enumeration import WebDriverType


class Element(Context):
    def __init__(self, parent):
        Context.__init__(self)
        # self
        self._inner_selenium_element = None
        self._locator = None
        self.__parent = parent

    def get_web_driver(self):
        """
            Get the web driver of this element.

        :return: the web driver
        """
        return self.get_parent().get_web_driver()

    def get_web_driver_type(self):
        """
            Get the type of this element's web driver.

        :return: the web driver type
        """
        return self.get_web_driver().get_web_driver_type()

    def get_parent(self):
        """
            Get the parent of this element.

        :return: the parent of this element
        """
        return self.__parent

    def _selenium_context(self):
        if self._inner_selenium_element is None:
            self._refresh()
        return self._inner_selenium_element

    def _selenium_element(self):
        if self._inner_selenium_element is None:
            self._refresh()
        return self._inner_selenium_element

    def wait_for(self, interval=None, timeout=None):
        """
            Get a ElementWaitFor instance.

        :param interval: the wait interval (in milliseconds). If None, use element's wait interval.
        :param timeout: the wait timeout (in milliseconds). If None, use element's wait timeout.
        """
        _interval = self.get_wait_interval() if interval is None else interval
        _timeout = self.get_wait_timeout() if timeout is None else timeout
        return ElementWaitFor(self, _interval, _timeout)

    def focus(self):
        """
            Focus this element.
        """
        try:
            try:
                self.get_web_driver().execute_script("arguments[0].focus()", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().execute_script("arguments[0].focus()", self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def blur(self):
        """
            Removes keyboard focus from this element.
        """
        try:
            try:
                self.get_web_driver().execute_script("arguments[0].blur()", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().execute_script("arguments[0].blur()", self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def clear(self):
        """
            Clears the text if it's a text entry element.
        """
        try:
            try:
                self._selenium_element().clear()
            except (NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException):
                self.wait_for().visible()
                self._selenium_element().clear()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def click(self):
        """
            Clicks this element.
        """
        try:
            try:
                self._selenium_element().click()
            except (NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException):
                self.wait_for().visible()
                self._selenium_element().click()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def double_click(self):
        """
            Double clicks this element.
        """
        try:
            try:
                self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
            except (NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException):
                self.wait_for().visible()
                self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def context_click(self):
        """
            Context click this element.
        """
        try:
            try:
                self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def send_keys(self, *value):
        """
            Simulates typing into this element.

        :param value: A string for typing, or setting form fields.  For setting
            file inputs, this could be a local file path. For special keys codes,
            use enum selenium.webdriver.common.Keys.

        Use this to send simple key events or to fill out form fields::

            form_textfield = driver.find_element('name=username')
            form_textfield.send_keys("admin")

        This can also be used to set file inputs::

            file_input = driver.find_element('name=profilePic')
            file_input.send_keys("path/to/profilepic.gif")
            # Generally it's better to wrap the file path in one of the methods
            # in os.path to return the actual path to support cross OS testing.
            # file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))

        """
        try:
            try:
                self._selenium_element().send_keys(*value)
            except (NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException):
                self.wait_for().visible()
                self._selenium_element().send_keys(*value)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def submit(self):
        """
            Submits a form.
        """
        try:
            try:
                self._selenium_element().submit()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().submit()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_attribute(self, name):
        """
            Gets the given attribute or property of the element.

            This method will first try to return the value of a property with the
            given name. If a property with that name doesn't exist, it returns the
            value of the attribute with the same name. If there's no attribute with
            that name, ``None`` is returned.

            Values which are considered truthy, that is equals "true" or "false",
            are returned as booleans.  All other non-``None`` values are returned
            as strings.  For attributes or properties which do not exist, ``None``
            is returned.

        :param name: Name of the attribute/property to retrieve.

        :Usage:
            # Check if the "active" CSS class is applied to an element.
            is_active = "active" in target_element.get_attribute("class")
        """
        try:
            try:
                return self._selenium_element().get_attribute(name)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute(name)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_css_value(self, property_name):
        """
            Gets the value of a CSS property.

        :param property_name: the property name
        """
        try:
            try:
                return self._selenium_element().value_of_css_property(property_name)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().value_of_css_property(property_name)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    get_value_of_css_property = get_css_value

    def get_location(self):
        """
            Gets the location for the top-left corner of this element.
        """
        try:
            try:
                return self._selenium_element().location
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().location
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_location_in_view(self):
        """
            Use this to discover where on the screen this element is.
            THIS METHOD SHOULD CAUSE THE ELEMENT TO BE SCROLLED INTO VIEW.

            Returns the top-left corner location on the screen, or ``None`` if
            this element is not visible.
        """
        web_driver_type = self.get_web_driver_type()
        try:
            try:
                if web_driver_type in WebDriverType._MOBILE:
                    return self._selenium_element().location_in_view
                else:
                    return self._selenium_element().location_once_scrolled_into_view
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                if web_driver_type in WebDriverType._MOBILE:
                    return self._selenium_element().location_in_view
                else:
                    return self._selenium_element().location_once_scrolled_into_view
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_size(self):
        """
            Gets the size (including border) of this element.
        """
        try:
            try:
                return self._selenium_element().size
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().size
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_rect(self):
        """
            Gets a dictionary with the size and location of this element.
        """
        try:
            try:
                if self.get_web_driver_type() == WebDriverType.FIREFOX:
                    return self._selenium_element().rect
                else:
                    rect = {}
                    rect.update(self._selenium_element().location)
                    rect.update(self._selenium_element().size)
                    return rect
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                if self.get_web_driver_type() == WebDriverType.FIREFOX:
                    return self._selenium_element().rect
                else:
                    rect = {}
                    rect.update(self._selenium_element().location)
                    rect.update(self._selenium_element().size)
                    return rect
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_center(self):
        """
            Gets the location for the center of this element.
        """
        rect = self.get_rect()
        return {"x": rect["x"] + rect["width"] / 2,
                "y": rect["y"] + rect["height"] / 2}

    def get_tag_name(self):
        """
            Gets this element's tagName property.
        """
        try:
            try:
                return self._selenium_element().tag_name
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().tag_name
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_value(self):
        """
            Gets the value of this element.
            Can be used to get the text of a text entry element.
            Text entry elements are INPUT and TEXTAREA elements.
        """
        try:
            try:
                return self._selenium_element().get_attribute("value")
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute("value")
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_text(self):
        """
            Gets the text of this element(including the text of its children).
        """
        try:
            try:
                return self._selenium_element().text
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().text
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

        if content is None:
            raise EasyiumException("Cannot get text content of a non-text node in element:", self)
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
            raise EasyiumException(wde.msg, self)

    def get_inner_html(self):
        """
            Get the inner html of this element.
        """
        try:
            try:
                return self.get_web_driver().execute_script("return arguments[0].innerHTML", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self.get_web_driver().execute_script("return arguments[0].innerHTML", self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def is_enabled(self):
        """
            Returns whether the element is enabled.
        """
        try:
            try:
                return self._selenium_element().is_enabled()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_enabled()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def is_selected(self):
        """
            Returns whether this element is selected.
            Can be used to check if a checkbox or radio button is selected.
        """
        try:
            try:
                return self._selenium_element().is_selected()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_selected()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverType._BROWSER)
    def mouse_over(self):
        """
            Do mouse over this element.
        """
        script = """
            var mouseoverEventObj = null;
            if (typeof window.Event == "function") {
                mouseoverEventObj = new MouseEvent('mouseover', {'bubbles': true, 'cancelable': true});
            } else {
                mouseoverEventObj = document.createEvent("MouseEvents");
                mouseoverEventObj.initMouseEvent("mouseover", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            }
            arguments[0].dispatchEvent(mouseoverEventObj);
        """
        try:
            try:
                self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self.get_web_driver().execute_script(script, self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverType._BROWSER)
    def mouse_out(self):
        """
            Do mouse out this element.
        """
        script = """
            var mouseoutEventObj = null;
            if (typeof window.Event == "function") {
                mouseoutEventObj = new MouseEvent('mouseout', {'bubbles': true, 'cancelable': true});
            } else {
                mouseoutEventObj = document.createEvent("MouseEvents");
                mouseoutEventObj.initMouseEvent("mouseout", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            }
            arguments[0].dispatchEvent(mouseoutEventObj);
        """
        try:
            try:
                self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                self.get_web_driver().execute_script(script, self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def drag_and_drop_by_offset(self, x_offset, y_offset):
        """
            Drag and drop to target offset.

        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        web_driver_type = self.get_web_driver_type()
        try:
            try:
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        x=x_offset, y=y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(
                        x_offset, y_offset).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        x=x_offset, y=y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(
                        x_offset, y_offset).release().perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

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
                        self._selenium_element()).move_to_element(target_element._selenium_element()).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element()).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(
                        self._selenium_element()).move_to_element(target_element._selenium_element()).release().perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def drag_and_drop_to_with_offset(self, target_element, x_offset, y_offset):
        """
            Drag and drop to target element with offset.
            The origin is at the top-left corner of web driver and offsets are relative to the top-left corner of the target element.

        :param target_element: the target element to drop
        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        web_driver_type = self.get_web_driver_type()
        try:
            try:
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                if web_driver_type in WebDriverType._MOBILE:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverType._MOBILE)
    def multiple_tap(self, count=1):
        """
            Perform a multiple-tap action on this element

        :param count: how many tap actions to perform on this element.
        """
        try:
            try:
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverType._MOBILE)
    def tap(self):
        """
            Perform a tap action on this element.
        """
        self.multiple_tap(1)

    @SupportedBy(WebDriverType._MOBILE)
    def double_tap(self):
        """
            Perform a double-tap action on this element.
        """
        self.multiple_tap(2)

    @SupportedBy(WebDriverType._MOBILE)
    def long_press(self, duration=1000):
        """
            Long press on this element.

        :param duration: the duration of long press lasts(in ms).
        """
        try:
            try:
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverType._MOBILE)
    def scroll(self, direction):
        """
            Scrolls to direction in this element.

        :param direction: the direction to scroll, the possible values are: up, down, left, right
        """
        try:
            try:
                scroll_params = {
                    "direction": direction,
                    "element": self._selenium_element().id
                }
                self.get_web_driver().execute_script("mobile: scroll", scroll_params)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().visible()
                scroll_params = {
                    "direction": direction,
                    "element": self._selenium_element().id
                }
                self.get_web_driver().execute_script("mobile: scroll", scroll_params)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

    def scroll_into_view(self):
        """
            Scrolls this element into view.
        """
        web_driver_type = self.get_web_driver_type()
        try:
            try:
                if web_driver_type in WebDriverType._MOBILE:
                    scroll_params = {
                        "element": self._selenium_element().id
                    }
                    self.get_web_driver().execute_script("mobile: scrollTo", scroll_params)
                else:
                    self.get_web_driver().execute_script("arguments[0].scrollIntoView();", self)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                if web_driver_type in WebDriverType._MOBILE:
                    scroll_params = {
                        "element": self._selenium_element().id
                    }
                    self.get_web_driver().execute_script("mobile: scrollTo", scroll_params)
                else:
                    self.get_web_driver().execute_script("arguments[0].scrollIntoView();", self)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

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
            raise EasyiumException(wde.msg, self)

    def get_screenshot_as_file(self, filename):
        """
            Gets the screenshot of the current element. Returns False if there is
            any IOError, else returns True. Use full paths in your filename.

        :param filename: The full path you wish to save your screenshot to.

        :Usage:
            element.get_screenshot_as_file('/Screenshots/foo.png')
        """
        try:
            try:
                return self._selenium_element().screenshot(filename)
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot(filename)
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_screenshot_as_png(self):
        """
            Gets the screenshot of the current element as a binary data.

        :Usage:
            element_png = element.get_screenshot_as_png()
        """
        try:
            try:
                return self._selenium_element().screenshot_as_png
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot_as_png
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_screenshot_as_base64(self):
        """
            Gets the screenshot of the current element as a base64 encoded string.

        :Usage:
            img_b64 = element.get_screenshot_as_base64()
        """
        try:
            try:
                return self._selenium_element().screenshot_as_base64
            except (NoSuchElementException, StaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot_as_base64
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    save_screenshot = get_screenshot_as_file

    def is_displayed(self):
        """
            Return whether this element is displayed or not.
        """
        try:
            try:
                return self._selenium_element().is_displayed()
            except StaleElementReferenceException:
                self._refresh()
                return self._selenium_element().is_displayed()
        except NoSuchElementException:
            return False
        except WebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def exists(self):
        """
            Return whether this element is existing or not.
        """
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
            raise EasyiumException(wde.msg, self)
