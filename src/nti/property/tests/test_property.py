#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import same_instance

import unittest

from nti.property.property import dict_alias, CachedProperty

class TestProperty(unittest.TestCase):

	def test_dict_alias(self):
		class X(object):
			def __init__(self):
				self.x = 1

			y = dict_alias('x')

		assert_that(X(), has_property('y', 1))
		x = X()
		x.y = 2
		assert_that(x, has_property('y', 2))
		assert_that(x, has_property('x', 2))

	def test_cached_property(self):

		# Usable directly

		class X(object):

			@CachedProperty
			def prop(self):
				return object()

		x = X()
		assert_that(x.prop, same_instance(x.prop))

		# Usable with names

		class Y(object):

			def __init__(self):
				self.dep = 1

			@CachedProperty('dep')
			def prop(self):
				return str(self.dep)

		y = Y()
		assert_that(y.prop, same_instance(y.prop))
		assert_that(y.prop, is_("1"))
		y.dep = 2
		assert_that(y.prop, is_("2"))
		assert_that(y.prop, same_instance(y.prop))

		# And, to help refactoring, usable with parens but no names
		class Z(object):
			@CachedProperty()
			def prop(self):
				return object()

		z = Z()
		assert_that(z.prop, same_instance(z.prop))
