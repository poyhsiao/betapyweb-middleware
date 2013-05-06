#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Diagnostic Tools
"""
import unittest
import threading
import ml_w_diagnostic_tools

class test_ping(unittest.TestCase):
	""" Test Diagnostic Tools """
	def setUp(self):
		""" setUp """

	def test_diagnostic_tools_g01(self):
		""" view_g01 """
		e = ml_w_diagnostic_tools.start_ping(None, "127.0.0.1", threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
