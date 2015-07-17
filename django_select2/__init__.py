# -*- coding: utf-8 -*-
"""
This is a Django_ integration of Select2_.

The app includes Select2 driven Django Widgets and Form Fields.

.. _Django: https://www.djangoproject.com/
.. _Select2: http://ivaynberg.github.com/select2/

Widgets
-------

These components are responsible for rendering the necessary JavaScript and HTML markups. Since this whole
package is to render choices using Select2 JavaScript library, hence these components are meant to be used
with choice fields.

Widgets are generally of two types :-

    1. **Light** --
    They are not meant to be used when there are too many options, say, in thousands. This
    is because all those options would have to be pre-rendered onto the page and JavaScript would
    be used to search through them. Said that, they are also one the most easiest to use. They are almost
    drop-in-replacement for Django's default select widgets.

    2. **Heavy** --
    They are suited for scenarios when the number of options are large and need complex queries
    (from maybe different sources) to get the options. This dynamic fetching of options undoubtedly requires
    Ajax communication with the server. Django-Select2 includes a helper JS file which is included automatically,
    so you need not worry about writing any Ajax related JS code. Although on the server side you do need to
    create a view specifically to respond to the queries.

    Heavies have further specialized versions called -- **Auto Heavy**. These do not require views to serve Ajax
    requests. When they are instantiated, they register themselves with one central view which handles Ajax requests
    for them.

Heavy widgets have the word 'Heavy' in their name. Light widgets are normally named, i.e. there is no 'Light' word
in their names.

**Available widgets:**

:py:class:`.Select2Widget`, :py:class:`.Select2MultipleWidget`, :py:class:`.HeavySelect2Widget`, :py:class:`.HeavySelect2MultipleWidget`,
:py:class:`.AutoHeavySelect2Widget`, :py:class:`.AutoHeavySelect2MultipleWidget`, :py:class:`.HeavySelect2TagWidget`,
:py:class:`.AutoHeavySelect2TagWidget`

`Read more`_

Fields
------

These are pre-implemented choice fields which use the above widgets. It is highly recommended that you use them
instead of rolling your own.

The fields available are good for general purpose use, although more specialized versions too are available for
your ease.

**Available fields:**

:py:class:`.Select2ChoiceField`, :py:class:`.Select2MultipleChoiceField`, :py:class:`.HeavySelect2ChoiceField`,
:py:class:`.HeavySelect2MultipleChoiceField`, :py:class:`.HeavyModelSelect2ChoiceField`,
:py:class:`.HeavyModelSelect2MultipleChoiceField`, :py:class:`.ModelSelect2Field`, :py:class:`.ModelSelect2MultipleField`,
:py:class:`.AutoSelect2Field`, :py:class:`.AutoSelect2MultipleField`, :py:class:`.AutoModelSelect2Field`,
:py:class:`.AutoModelSelect2MultipleField`, :py:class:`.HeavySelect2TagField`, :py:class:`.AutoSelect2TagField`,
:py:class:`.HeavyModelSelect2TagField`, :py:class:`.AutoModelSelect2TagField`

Views
-----

The view - `Select2View`, exposed here is meant to be used with 'Heavy' fields and widgets.

**Imported:**

:py:class:`.Select2View`, :py:data:`.NO_ERR_RESP`

`Read more`_

.. _Read more: http://blog.applegrew.com/2012/08/django-select2/

"""
from __future__ import absolute_import, unicode_literals

import logging
import warnings

from .types import NO_ERR_RESP  # NOAQ

logger = logging.getLogger(__name__)


__version__ = "4.3.1"

__RENDER_SELECT2_STATICS = False
__BOOTSTRAP = False

# @todo: Deprecated and to be removed in v5
__ENABLE_MULTI_PROCESS_SUPPORT = False
__MEMCACHE_HOST = None
__MEMCACHE_PORT = None
__MEMCACHE_TTL = 900
__GENERATE_RANDOM_ID = False


try:
    from django.conf import settings
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Django found.")
    if settings.configured:
        __RENDER_SELECT2_STATICS = getattr(settings, 'AUTO_RENDER_SELECT2_STATICS', True)
        __ENABLE_MULTI_PROCESS_SUPPORT = getattr(settings, 'ENABLE_SELECT2_MULTI_PROCESS_SUPPORT', False)
        __MEMCACHE_HOST = getattr(settings, 'SELECT2_MEMCACHE_HOST', None)
        __MEMCACHE_PORT = getattr(settings, 'SELECT2_MEMCACHE_PORT', None)
        __MEMCACHE_TTL = getattr(settings, 'SELECT2_MEMCACHE_TTL', 900)
        __GENERATE_RANDOM_ID = getattr(settings, 'GENERATE_RANDOM_SELECT2_ID', False)
        __BOOTSTRAP = getattr(settings, 'SELECT2_BOOTSTRAP', False)

        if __GENERATE_RANDOM_ID:
            msg = (
                'Select2\'s setting "GENERATE_RANDOM_SELECT2_ID" has been deprecated.\n'
                'Since version 4.4 all IDs will be encrypted by default.'
            )
            warnings.warn(msg, DeprecationWarning)
            __ENABLE_MULTI_PROCESS_SUPPORT = False
        if __ENABLE_MULTI_PROCESS_SUPPORT:
            msg = (
                'Select2\'s setting "ENABLE_SELECT2_MULTI_PROCESS_SUPPORT"'
                ' has been deprecated and will be removed in version 4.4.\n'
                'Multiprocessing support is on by default.\n'
                'If you seek multi machine support please review the latest documentation.'
            )
            warnings.warn(msg, DeprecationWarning)
        if __MEMCACHE_HOST or __MEMCACHE_PORT or __MEMCACHE_TTL:
            msg = (
                'Select2\'s setting "SELECT2_MEMCACHE_HOST" has been deprecated'
                ' in favour of "SELECT2_CACHE_BACKEND".\n'
                'The support for this setting will be removed in version 5.'
            )

        from .widgets import (
            Select2Widget, Select2MultipleWidget,
            HeavySelect2Widget, HeavySelect2MultipleWidget,
            AutoHeavySelect2Widget, AutoHeavySelect2MultipleWidget,
            HeavySelect2TagWidget, AutoHeavySelect2TagWidget
        )  # NOQA
        from .fields import (
            Select2ChoiceField, Select2MultipleChoiceField,
            HeavySelect2ChoiceField, HeavySelect2MultipleChoiceField,
            HeavyModelSelect2ChoiceField, HeavyModelSelect2MultipleChoiceField,
            ModelSelect2Field, ModelSelect2MultipleField,
            AutoSelect2Field, AutoSelect2MultipleField,
            AutoModelSelect2Field, AutoModelSelect2MultipleField,
            HeavySelect2TagField, AutoSelect2TagField,
            HeavyModelSelect2TagField, AutoModelSelect2TagField
        )  # NOQA
        from .views import Select2View

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Django found and fields and widgets loaded.")
except ImportError:
    if logger.isEnabledFor(logging.INFO):
        logger.info("Django not found.")
