#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Rates
"""
import unittest
import threading
import ml_w_rates

class test_get(unittest.TestCase):
	""" Test Rates """
	def setUp(self):
		""" setUp """

	def test_rates_g01(self):
		""" rates_g01 """
		e = ml_w_rates.get(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
