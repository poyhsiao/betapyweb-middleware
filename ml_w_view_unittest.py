#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - View
"""
import unittest
import threading
import ml_w_view

class test_refresh(unittest.TestCase):
	""" Test View """
	def setUp(self):
		""" setUp """

	def test_view_g01(self):
		""" view_g01 """
		e = ml_w_view.refresh(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
