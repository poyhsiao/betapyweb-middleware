#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - check
"""
import unittest
import ml_check

class test_validate_ipv4(unittest.TestCase):
	""" Test validate_ipv4() """
	def setUp(self):
		""" setUp """

	def test_validate_ipv4_g01(self):
		""" validate_ipv4_g01 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv4("10.12.97.100"))

	def test_validate_ipv4_g02(self):
		""" validate_ipv4_g02 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv4("0.0.0.0"))

	def test_validate_ipv4_g03(self):
		""" validate_ipv4_g03 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv4("255.255.255.255"))

	def test_validate_ipv4_b04(self):
		""" validate_ipv4_b04 """
		self.maxDiff = None
		self.assertFalse(ml_check.validate_ipv4("a.b.c.d"))

	def test_validate_ipv4_b05(self):
		""" validate_ipv4_b05 """
		self.maxDiff = None
		self.assertFalse(ml_check.validate_ipv4("1.2.3.256"))

	def test_validate_ipv4_b06(self):
		""" validate_ipv4_b06 """
		self.maxDiff = None
		self.assertFalse(ml_check.validate_ipv4("-1.0.1.2"))

	def test_validate_ipv4_netmask_g01(self):
		""" validate_ipv4_netmask_g01 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv4_netmask("255.255.255.255"))

	def test_validate_ipv6_g01(self):
		""" validate_ipv6_g01 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv6("2001::1"))

	def test_validate_ipv6_b02(self):
		""" validate_ipv6_b02 """
		self.maxDiff = None
		self.assertFalse(ml_check.validate_ipv6("x:y:z"))

	def test_validate_ipv6_prefix_g01(self):
		""" validate_ipv6_prefix_g01 """
		self.maxDiff = None
		self.assertTrue(ml_check.validate_ipv6_prefix(64))

if __name__ == "__main__":
	unittest.main()
