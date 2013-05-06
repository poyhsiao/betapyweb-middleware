#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Routing Table
"""
import unittest
import os
import threading
import ml_w_routing_table
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_routing_table_g01(self):
		""" routing_table_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "routing_table-g01.json"), os.path.join("running", "routing_table.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "routing_table-g01.jcfg"), os.path.join("running", "routing_table.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_routing_table.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"ipv4": [
				{
					"destination": "192.168.0.0",
					"prefix": 24,
					"gateway": "192.168.0.254",
					"interface": "s0e1"
				}
			],
			"ipv6": [
				{
					"destination": "2001::",
					"prefix": 64,
					"gateway": "2001::2001",
					"interface": "s0e1"
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_routing_table_g02(self):
		""" routing_table_g02 """
		routing_table = {
			"ipv4": [
				{
					"destination": "192.168.0.0",
					"prefix": 24,
					"gateway": "192.168.0.254",
					"interface": "s0e1"
				}
			],
			"ipv6": [
				{
					"destination": "2001::",
					"prefix": 64,
					"gateway": "2001::2001",
					"interface": "s0e1"
				}
			]
		}
		self.maxDiff = None
		e = ml_w_routing_table.set(None, routing_table)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "routing_table.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ipv4": [{"interface": "s0e1", "prefix": 24, "destination": "192.168.0.0", "gateway": "192.168.0.254"}], "ipv6": [{"interface": "s0e1", "prefix": 64, "destination": "2001::", "gateway": "2001::2001"}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['routing_table {\n', '    ipv4-array {\n', '        ipv4 { #1\n', '            destination 192.168.0.0\n', '            gateway 192.168.0.254\n', '        }\n', '    }\n', '    ipv6-array {\n', '        ipv6 { #1\n', '            destination 2001::\n', '            gateway 2001::2001\n', '        }\n', '    }\n', '}\n'])

	def test_routing_table_g03(self):
		""" routing_table_g03 """
		routing_table = {
			"ipv4": [
				{
					"destination": "192.168.0.0",
					"prefix": 24,
					"gateway": "192.168.0.254",
					"interface": "s0e1"
				}
			],
			"ipv6": [
				{
					"destination": "2001::",
					"prefix": 64,
					"gateway": "2001::2001",
					"interface": "s0e1"
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_routing_table.set(None, routing_table, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "routing_table.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ipv4": [{"interface": "s0e1", "prefix": 24, "destination": "192.168.0.0", "gateway": "192.168.0.254"}], "ipv6": [{"interface": "s0e1", "prefix": 64, "destination": "2001::", "gateway": "2001::2001"}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['routing_table {\n', '    ipv4-array {\n', '        ipv4 { #1\n', '            destination 192.168.0.0\n', '            gateway 192.168.0.254\n', '        }\n', '    }\n', '    ipv6-array {\n', '        ipv6 { #1\n', '            destination 2001::\n', '            gateway 2001::2001\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
