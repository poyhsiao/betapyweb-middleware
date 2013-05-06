#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Counters
"""
import unittest
import threading
import ml_w_counters

class test_get(unittest.TestCase):
	""" Test Counters """
	def setUp(self):
		""" setUp """

	def test_counters_g01(self):
		""" counters_g01 """
		e = ml_w_counters.get(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
