#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Persistence Info
"""
import unittest
import threading
import ml_w_persistence_info

class test_get(unittest.TestCase):
	""" Test Persistence Info """
	def setUp(self):
		""" setUp """

	def test_persistence_info_g01(self):
		""" persistence_info_g01 """
		e = ml_w_persistence_info.get(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
