=======
easyium
=======
easyium is an easy-to-use wrapper for selenium&appium and it can make you more focus on business not the element.

Find the latest version on github: https://github.com/KarlGong/easyium-python or PyPI: https://pypi.python.org/pypi/easyium

Advantages
----------
- easyium provides unified apis to test on browsers and devices.

- easyium adds a global implicit wait for elements and you rarely need to consider waiting a element to be visible or existing.

- easyium introduces a simple and clear way to build model objects for UI.

- easyium has a better performance, the element will lazily load WebElement reference and reuses it if necessary.

- easyium provides easy-to-use wait method for element. e.g., my_element.wait_for().not_().exists()

- easyium provides a simple way to define a locator. e.g., use ``"xpath=.//mytag"`` instead of ``By.XPATH, ".//mytag"``

- easyium provides a mechanism to avoid StaleElementReferenceException.

Installation
------------
The last stable release is available on PyPI and can be installed with ``pip``.

::

    $ pip install easyium

Glossary
--------
WebDriver
~~~~~~~~~
It is a wrapper for selenium&appium's web driver. You can create a new instance by providing web driver type.

DynamicElement
~~~~~~~~~~~~~~
DynamicElement is one type of Element in easyium. It refers to the element which is dynamic relative to its parent.

You can get it only by calling ``WebDriver.find_element(locator)`` or ``Element.find_element(locator)`` and you can not create a new instance by yourself.

StaticElement
~~~~~~~~~~~~~
StaticElement is the other type of Element in easyium. It refers to the element which is static relative to its parent.

You can create a new instance by providing parent and locator.

Example
-------
For detailed examples, please refer to the ``examples`` folder in source distribution or visit https://github.com/KarlGong/easyium-python/tree/master/examples

Contact me
----------
For information and suggestions you can contact me at karl.gong@outlook.com

Change Log
----------
1.1.5 (compared to 1.1.4)

- Add scroll(), switch_to_new_window() to WebDriver.

- Add scroll(), scroll_into_view() to Element.

- Raise InvalidLocatorException when the locator is invalid.

1.1.4 (compared to 1.1.3)

- Add get_screenshot_as_xxx() to Element.

1.1.3 (compared to 1.1.2)

- Add docstring for apis.

- Add post wait time for waiter.

1.1.2 (compared to 1.1.1)

- Add pre wait time for waiter.

1.1.1 (compared to 1.1.0)

- Optimize the waiter.

- Add blur() for class Element.

1.1.0 (compared to 1.0.0)

- Refactor the waiter.

1.0.0

- Baby easyium.