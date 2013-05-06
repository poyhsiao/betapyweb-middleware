#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Bridge
"""
import unittest
import os
import threading
import ml_w_bridge
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test Bridge """
	def setUp(self):
		""" setUp """

	def test_bridge_g01(self):
		""" bridge_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "bridge-g01.json"), os.path.join("running", "bridge.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "bridge-g01.jcfg"), os.path.join("running", "bridge.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_bridge.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"br": [
				{
					"name": "s0b1",
					"interface": [
						"s0e2"
					],
					"STP": True,
					"hello_time": 5,
					"max_message_age": 5,
					"forward_delay": 5
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test Bridge """
	def setUp(self):
		""" setUp """

	def test_bridge_g02(self):
		""" bridge_g02 """
		bridge = {
			"br": [
				{
					"name": "s0b1",
					"interface": [
						"s0e2"
					],
					"STP": True,
					"hello_time": 5,
					"max_message_age": 5,
					"forward_delay": 5
				}
			]
		}
		self.maxDiff = None
		e = ml_w_bridge.set(None, bridge)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "bridge.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['bridge {\n', '    br-array {\n', '        br { #1\n', '            name s0b1\n', '            interface-array {\n', '                interface s0e2 #1\n', '            }\n', '            hello_time 5\n', '            max_message_age 5\n', '            forward_delay 5\n', '        }\n', '    }\n', '}\n'])

	def test_bridge_g03(self):
		""" bridge_g03 """
		bridge = {
			"br": [
				{
					"name": "s0b1",
					"interface": [
						"s0e2"
					],
					"STP": True,
					"hello_time": 5,
					"max_message_age": 5,
					"forward_delay": 5
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_bridge.set(None, bridge, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "bridge.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['bridge {\n', '    br-array {\n', '        br { #1\n', '            name s0b1\n', '            interface-array {\n', '                interface s0e2 #1\n', '            }\n', '            hello_time 5\n', '            max_message_age 5\n', '            forward_delay 5\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
