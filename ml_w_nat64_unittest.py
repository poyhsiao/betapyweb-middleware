#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - NAT64
"""
import unittest
import os
import threading
import shutil
import ml_w_nat64
import ml_system

class test_get(unittest.TestCase):
	""" Test NAT64 """
	def setUp(self):
		""" setUp """

	def test_nat64_g01(self):
		""" nat64_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "nat64-g01.json"), os.path.join("running", "nat64.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "nat64-g01.jcfg"), os.path.join("running", "nat64.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_nat64.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"enable": True,
			"ipv6": "64:ff9b::",
			"ipv6_prefix": 96,
			"ipv4": "0.0.0.0"
		}))

class test_set(unittest.TestCase):
	""" Test NAT64 """
	def setUp(self):
		""" setUp """

	def test_nat64_g02(self):
		""" nat64_g02 """
		nat64 = {
			"enable": True,
			"ipv6": "64:ff9b::",
			"ipv6_prefix": 96,
			"ipv4": "0.0.0.0"
		}
		self.maxDiff = None
		e = ml_w_nat64.set(None, nat64)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "nat64.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['nat64 {\n', '    enable True\n', '}\n'])

	def test_nat64_g03(self):
		""" nat64_g03 """
		nat64 = {
			"enable": True,
			"ipv6": "64:ff9b::",
			"ipv6_prefix": 96,
			"ipv4": "0.0.0.0"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_nat64.set(None, nat64, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "nat64.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['nat64 {\n', '    enable True\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
