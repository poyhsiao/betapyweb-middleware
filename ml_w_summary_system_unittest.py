#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Summary System
"""
import unittest
import threading
import ml_w_summary_system

class test_get(unittest.TestCase):
	""" Test Summary System """
	def setUp(self):
		""" setUp """

	def test_summary_system_g01(self):
		""" summary_system_g01 """
		e = ml_w_summary_system.get(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
