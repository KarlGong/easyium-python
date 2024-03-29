from typing import Union

from appium.webdriver.webelement import WebElement as AppiumElement
from selenium.common.exceptions import WebDriverException as SeleniumWebDriverException, StaleElementReferenceException as SeleniumStaleElementReferenceException, \
    InvalidElementStateException as SeleniumInvalidElementStateException

from .context import Context
from .decorator import SupportedBy
from .enumeration import WebDriverContext, WebDriverPlatform
from .exceptions import EasyiumException, NoSuchElementException
from .waiter import ElementWaitFor
from .web_driver import WebDriver, WebDriverInfo


class Element(Context):
    def __init__(self, parent: Context):
        Context.__init__(self)
        # self
        self._inner_selenium_element = None
        self._locator = None
        self.__parent = parent

    def get_web_driver(self) -> WebDriver:
        """
            Get the web driver of this element.

        :return: the web driver
        """
        return self.get_parent().get_web_driver()

    def get_web_driver_info(self) -> WebDriverInfo:
        """
            Get current info of this web driver.

        :return: the web driver info
        """
        return self.get_web_driver().get_web_driver_info()

    def get_parent(self) -> Context:
        """
            Get the parent of this element.

        :return: the parent of this element
        """
        return self.__parent

    def _selenium_context(self) -> AppiumElement:
        if self._inner_selenium_element is None:
            self._refresh()
        return self._inner_selenium_element

    def _selenium_element(self) -> AppiumElement:
        if self._inner_selenium_element is None:
            self._refresh()
        return self._inner_selenium_element

    def wait_for(self, interval: int = None, timeout: int = None) -> ElementWaitFor:
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
            self.get_web_driver().execute_script("arguments[0].focus()", self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def blur(self):
        """
            Removes keyboard focus from this element.
        """
        try:
            self.get_web_driver().execute_script("arguments[0].blur()", self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def clear(self):
        """
            Clears the text if it's a text entry element.
        """
        try:
            try:
                self._selenium_element().clear()
            except (NoSuchElementException, SeleniumStaleElementReferenceException, SeleniumInvalidElementStateException):
                self.wait_for().visible()
                self._selenium_element().clear()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def click(self):
        """
            Clicks this element.
        """
        try:
            try:
                self._selenium_element().click()
            except (NoSuchElementException, SeleniumStaleElementReferenceException, SeleniumInvalidElementStateException):
                self.wait_for().visible()
                self._selenium_element().click()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def double_click(self):
        """
            Double click this element.
        """
        script = """
            var dblclickEventObj = null;
            if (typeof window.Event == "function") {
                dblclickEventObj = new MouseEvent('dblclick', {'bubbles': true, 'cancelable': true});
            } else {
                dblclickEventObj = document.createEvent("MouseEvents");
                dblclickEventObj.initMouseEvent('dblclick', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            }
            arguments[0].dispatchEvent(dblclickEventObj);
        """
        try:
            try:
                if self.get_web_driver_info().context == WebDriverContext.SAFARI \
                        and self.get_web_driver_info().platform == WebDriverPlatform.PC:
                    self.get_web_driver().execute_script(script, self)
                else:
                    self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException, SeleniumInvalidElementStateException):
                self.wait_for().visible()
                if self.get_web_driver_info().context == WebDriverContext.SAFARI \
                        and self.get_web_driver_info().platform == WebDriverPlatform.PC:
                    self.get_web_driver().execute_script(script, self)
                else:
                    self.get_web_driver().create_action_chains().double_click(self._selenium_element()).perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def context_click(self):
        """
            Context click this element.
        """
        script = """
            var clickEventObj = null;
            if (typeof window.Event == "function") {
                clickEventObj = new MouseEvent('click', {'bubbles': true, 'cancelable': true, 'button': 2, 'buttons': 2});
            } else {
                clickEventObj = document.createEvent("MouseEvents");
                clickEventObj.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 2, 2);
            }
            arguments[0].dispatchEvent(clickEventObj);
        """
        try:
            try:
                if self.get_web_driver_info().context == WebDriverContext.SAFARI \
                        and self.get_web_driver_info().platform == WebDriverPlatform.PC:
                    self.get_web_driver().execute_script(script, self)
                else:
                    self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                if self.get_web_driver_info().context == WebDriverContext.SAFARI \
                        and self.get_web_driver_info().platform == WebDriverPlatform.PC:
                    self.get_web_driver().execute_script(script, self)
                else:
                    self.get_web_driver().create_action_chains().context_click(self._selenium_element()).perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def send_keys(self, *value: str):
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
            except (NoSuchElementException, SeleniumStaleElementReferenceException, SeleniumInvalidElementStateException):
                self.wait_for().visible()
                self._selenium_element().send_keys(*value)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def submit(self):
        """
            Submits a form.
        """
        try:
            try:
                self._selenium_element().submit()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                self._selenium_element().submit()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_property(self, name: str) -> str:
        """
            Gets the given property of the element.

        :param name: Name of the property to retrieve.

        :Usage:
            text_length = target_element.get_property("text_length")
        """
        try:
            try:
                return self._selenium_element().get_property(name)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_property(name)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_dom_attribute(self, name: str) -> str:
        """
            Gets the given attribute of the element. Unlike :func:`get_attribute`, this method only returns attributes declared in the element's HTML markup.

        :param name: Name of the attribute to retrieve.

        :Usage:
            cls = target_element.get_dom_attribute("class")
        """
        try:
            try:
                return self._selenium_element().get_dom_attribute(name)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_dom_attribute(name)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_attribute(self, name: str) -> Union[str, bool]:
        """
            Gets the given attribute or property of this element.

            This method will first try to return the value of a property with the
            given name. If a property with that name doesn't exist, it returns the
            value of the attribute with the same name. If there's no attribute with
            that name, ``None`` is returned.

            Values which are considered truthy, that is equals "true" or "false",
            are returned as booleans.  All other non-``None`` values are returned
            as strings.  For attributes or properties which do not exist, ``None``
            is returned.

        :param name: name of the attribute/property to retrieve.

        :Usage:
            # Check if the "active" CSS class is applied to an element.
            is_active = "active" in target_element.get_attribute("class")
        """
        try:
            try:
                return self._selenium_element().get_attribute(name)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute(name)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def set_attribute(self, name: str, value: str):
        """
            Set the attribute of this element to value.
            
        :param name: the attribute name
        :param value: the value to be set
        """
        try:
            self.get_web_driver().execute_script("arguments[0].setAttribute('%s', '%s')" % (name, value), self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_css_value(self, property_name: str) -> str:
        """
            Gets the value of a CSS property.

        :param property_name: the property name
        """
        try:
            try:
                return self._selenium_element().value_of_css_property(property_name)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().value_of_css_property(property_name)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_value_of_css_property(self, property_name: str) -> str:
        """
            Gets the value of a CSS property.

        :param property_name: the property name
        """
        return self.get_css_value(property_name)

    def get_location(self) -> dict:
        """
            Gets the location for the top-left corner of this element.

        :return: the location dict, {'x': x, 'y': y}
        """
        try:
            try:
                return self._selenium_element().location
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().location
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_location_in_view(self) -> dict:
        """
            Use this to discover where on the screen this element is.
            THIS METHOD SHOULD CAUSE THE ELEMENT TO BE SCROLLED INTO VIEW.

            Returns the top-left corner location on the screen, or ``None`` if
            this element is not visible.
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    return self._selenium_element().location_in_view
                else:
                    return self._selenium_element().location_once_scrolled_into_view
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if context == WebDriverContext.NATIVE_APP:
                    return self._selenium_element().location_in_view
                else:
                    return self._selenium_element().location_once_scrolled_into_view
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_size(self) -> dict:
        """
            Gets the size (including border) of this element.

        :return: the size dict, {'width': width, 'height': height}
        """
        try:
            try:
                return self._selenium_element().size
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().size
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_rect(self) -> dict:
        """
            Gets a dictionary with the size and location of this element.

        :return: the rect dict, {'width': width, 'height': height, 'x': x, 'y': y}
        """
        try:
            try:
                return self._selenium_element().rect
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().rect
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_center(self) -> dict:
        """
            Gets the location for the center of this element.

        :return: the location dict, {'x': x, 'y': y}
        """
        rect = self.get_rect()
        return {"x": rect["x"] + rect["width"] / 2,
                "y": rect["y"] + rect["height"] / 2}

    def get_tag_name(self) -> str:
        """
            Gets this element's tagName property.
        """
        try:
            try:
                return self._selenium_element().tag_name
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().tag_name
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_value(self) -> str:
        """
            Gets the value of this element.
            Can be used to get the text of a text entry element.
            Text entry elements are INPUT and TEXTAREA elements.
        """
        try:
            try:
                return self._selenium_element().get_attribute("value")
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().get_attribute("value")
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def set_value(self, value: str):
        """
            Set the value on this element.

        :param value: the value to be set on this element
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    self._selenium_element().set_value(value)
                else:
                    self.get_web_driver().execute_script("arguments[0].setAttribute('value', '%s')" % value, self)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if context == WebDriverContext.NATIVE_APP:
                    self._selenium_element().set_value(value)
                else:
                    self.get_web_driver().execute_script("arguments[0].setAttribute('value', '%s')" % value, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_text(self) -> str:
        """
            Gets the text of this element(including the text of its children).
        """
        try:
            try:
                return self._selenium_element().text
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().text
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def set_text(self, text: str):
        """
            Sends text to this element. Previous text is removed.

        :param text: the text to be sent to this element
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    self._selenium_element().set_text(text)
                else:
                    self.get_web_driver().execute_script("arguments[0].innerText = '%s'" % text, self)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if context == WebDriverContext.NATIVE_APP:
                    self._selenium_element().set_text(text)
                else:
                    self.get_web_driver().execute_script("arguments[0].innerText = '%s'" % text, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_text_node_content(self, text_node_index: int) -> str:
        """
            Get content of the text node in this element.
            If the text_node_index refers to a non-text node or be out of bounds, an exception will be thrown.

        :param text_node_index: index of text node in this element
        :return: the content of the text node in this element.
        """
        try:
            content = self.get_web_driver().execute_script(
                "return arguments[0].childNodes[%s].nodeValue" % text_node_index, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

        if content is None:
            raise EasyiumException("Cannot get text content of a non-text node in element:", self)
        return content

    def set_selection_range(self, start: int, end: int):
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
                                    (start == endCharCount && i <= textNodes.length))) {
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
            self.get_web_driver().execute_script(script % (start, end), self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_inner_html(self) -> str:
        """
            Get the inner html of this element.
        """
        try:
            return self.get_web_driver().execute_script("return arguments[0].innerHTML", self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def is_enabled(self) -> bool:
        """
            Returns whether the element is enabled.
        """
        try:
            try:
                return self._selenium_element().is_enabled()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_enabled()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def is_selected(self) -> bool:
        """
            Returns whether this element is selected.
            Can be used to check if a checkbox or radio button is selected.
        """
        try:
            try:
                return self._selenium_element().is_selected()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                return self._selenium_element().is_selected()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def mouse_over(self, native: bool = False):
        """
            Do mouse over this element.
        
        :param native: use the selenium native implementation
        """
        script = """
            var mouseoverEventObj = null;
            if (typeof window.Event == "function") {
                mouseoverEventObj = new MouseEvent('mouseover', {'bubbles': true, 'cancelable': true});
            } else {
                mouseoverEventObj = document.createEvent("MouseEvents");
                mouseoverEventObj.initMouseEvent('mouseover', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            }
            arguments[0].dispatchEvent(mouseoverEventObj);
        """
        try:
            try:
                if native:
                    self.get_web_driver().create_action_chains().move_to_element(self._selenium_element()).perform()
                else:
                    self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if native:
                    self.get_web_driver().create_action_chains().move_to_element(self._selenium_element()).perform()
                else:
                    self.get_web_driver().execute_script(script, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def mouse_out(self, native: bool = False):
        """
            Do mouse out this element.
            
        :param native: use the selenium native implementation
        """
        script = """
            var mouseoutEventObj = null;
            if (typeof window.Event == "function") {
                mouseoutEventObj = new MouseEvent('mouseout', {'bubbles': true, 'cancelable': true});
            } else {
                mouseoutEventObj = document.createEvent("MouseEvents");
                mouseoutEventObj.initMouseEvent('mouseout', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            }
            arguments[0].dispatchEvent(mouseoutEventObj);
        """
        try:
            try:
                if native:
                    self.get_web_driver().create_action_chains().move_by_offset(-99999, -99999).perform()
                else:
                    self.get_web_driver().execute_script(script, self)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if native:
                    self.get_web_driver().create_action_chains().move_by_offset(-99999, -99999).perform()
                else:
                    self.get_web_driver().execute_script(script, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def drag_and_drop_by_offset(self, x_offset: float, y_offset: float):
        """
            Drag and drop to target offset.

        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        x=x_offset, y=y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(
                        x_offset, y_offset).release().perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        x=x_offset, y=y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_by_offset(
                        x_offset, y_offset).release().perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def drag_and_drop_to(self, target_element: "Element"):
        """
            Drag and drop to target element.

        :param target_element: the target element to drop
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element()).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(
                        self._selenium_element()).move_to_element(target_element._selenium_element()).release().perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element()).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(
                        self._selenium_element()).move_to_element(target_element._selenium_element()).release().perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def drag_and_drop_to_with_offset(self, target_element: "Element", x_offset: float, y_offset: float):
        """
            Drag and drop to target element with offset.
            The origin is at the top-left corner of web driver and offsets are relative to the top-left corner of the target element.

        :param target_element: the target element to drop
        :param x_offset: X offset to drop
        :param y_offset: Y offset to drop
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                target_element.wait_for().visible()
                if context == WebDriverContext.NATIVE_APP:
                    self.get_web_driver().create_touch_action().long_press(self._selenium_element()).move_to(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
                else:
                    self.get_web_driver().create_action_chains().click_and_hold(self._selenium_element()).move_to_element_with_offset(
                        target_element._selenium_element(), x_offset, y_offset).release().perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def multiple_tap(self, count: int = 1):
        """
            Perform a multiple-tap action on this element

        :param count: how many tap actions to perform on this element.
        """
        try:
            try:
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().tap(self._selenium_element(), None, None, count).perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def tap(self):
        """
            Perform a tap action on this element.
        """
        self.multiple_tap(1)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def double_tap(self):
        """
            Perform a double-tap action on this element.
        """
        self.multiple_tap(2)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def long_press(self, duration: int = 1000):
        """
            Long press on this element.

        :param duration: the duration of long press lasts(in ms).
        """
        try:
            try:
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver().create_touch_action().long_press(self._selenium_element(), None, None, duration).release().perform()
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def scroll(self, direction: str):
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
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                scroll_params = {
                    "direction": direction,
                    "element": self._selenium_element().id
                }
                self.get_web_driver().execute_script("mobile: scroll", scroll_params)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def scroll_into_view(self):
        """
            Scrolls this element into view.
        """
        context = self.get_web_driver_info().context
        try:
            try:
                if context == WebDriverContext.NATIVE_APP:
                    scroll_params = {
                        "element": self._selenium_element().id
                    }
                    self.get_web_driver().execute_script("mobile: scrollTo", scroll_params)
                else:
                    self.get_web_driver().execute_script("arguments[0].scrollIntoView();", self)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                if context == WebDriverContext.NATIVE_APP:
                    scroll_params = {
                        "element": self._selenium_element().id
                    }
                    self.get_web_driver().execute_script("mobile: scrollTo", scroll_params)
                else:
                    self.get_web_driver().execute_script("arguments[0].scrollIntoView();", self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def scroll_to(self, target_element: "Element", duration: int = None):
        """
            Scrolls from this element to another.

        :param target_element: the target element to be scrolled to
        :param duration: a duration after press and move to target element. Default is 600 ms for W3C spec. Zero for MJSONWP.
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().scroll(self._selenium_element(), target_element._selenium_element(), duration)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                target_element.wait_for().exists()
                self.get_web_driver()._selenium_web_driver().scroll(self._selenium_element(), target_element._selenium_element(), duration)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def pinch(self, percent: int = 200, steps: int = 50):
        """
            Pinch on this element a certain amount

        :param percent: amount to pinch. Defaults to 200%
        :param steps: number of steps in the pinch action
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().pinch(self._selenium_element(), percent, steps)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver()._selenium_web_driver().pinch(self._selenium_element(), percent, steps)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def zoom(self, percent: int = 200, steps: int = 50):
        """
            Zooms in on an element a certain amount.

        :param percent: amount to zoom. Defaults to 200%
        :param steps: number of steps in the zoom action
        """
        try:
            try:
                self.get_web_driver()._selenium_web_driver().zoom(self._selenium_element(), percent, steps)
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().visible()
                self.get_web_driver()._selenium_web_driver().zoom(self._selenium_element(), percent, steps)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_screenshot_as_file(self, filename: str) -> bool:
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
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot(filename)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def save_screenshot(self, filename: str) -> bool:
        """
            Gets the screenshot of the current element. Returns False if there is
            any IOError, else returns True. Use full paths in your filename.

        :param filename: The full path you wish to save your screenshot to.

        :Usage:
            element.save_screenshot('/Screenshots/foo.png')
        """
        return self.get_screenshot_as_file(filename)

    def get_screenshot_as_png(self) -> bytes:
        """
            Gets the screenshot of the current element as a binary data.

        :Usage:
            element_png = element.get_screenshot_as_png()
        """
        try:
            try:
                return self._selenium_element().screenshot_as_png
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot_as_png
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def get_screenshot_as_base64(self) -> str:
        """
            Gets the screenshot of the current element as a base64 encoded string.

        :Usage:
            img_b64 = element.get_screenshot_as_base64()
        """
        try:
            try:
                return self._selenium_element().screenshot_as_base64
            except (NoSuchElementException, SeleniumStaleElementReferenceException):
                self.wait_for().exists()
                return self._selenium_element().screenshot_as_base64
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def is_displayed(self) -> bool:
        """
            Return whether this element is displayed or not.
        """
        try:
            try:
                return self._selenium_element().is_displayed()
            except SeleniumStaleElementReferenceException:
                self._refresh()
                return self._selenium_element().is_displayed()
        except NoSuchElementException:
            return False
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def exists(self) -> bool:
        """
            Return whether this element is existing or not.
        """
        try:
            try:
                self._selenium_element().is_displayed()
                return True
            except SeleniumStaleElementReferenceException:
                self._refresh()
                return True
        except NoSuchElementException:
            return False
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)
