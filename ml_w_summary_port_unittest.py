#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Summary Port
"""
import unittest
import threading
import ml_w_summary_port

class test_get(unittest.TestCase):
	""" Test Summary Port """
	def setUp(self):
		""" setUp """

	def test_summary_port_g01(self):
		""" summary_port_g01 """
		e = ml_w_summary_port.get(None, threading.RLock())
		self.assertTrue(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
