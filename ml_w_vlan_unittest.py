#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - VLAN
"""
import unittest
import os
import threading
import ml_w_vlan
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test VLAN """
	def setUp(self):
		""" setUp """

	def test_vlan_g01(self):
		""" vlan_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "vlan-g01.json"), os.path.join("running", "vlan.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "vlan-g01.jcfg"), os.path.join("running", "vlan.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_vlan.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"vconfig": [
				{
					"interface": "s0e2",
					"vlan_id": 10
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test VLAN """
	def setUp(self):
		""" setUp """

	def test_vlan_g02(self):
		""" vlan_g02 """
		vlan = {
			"vconfig": [
				{
					"interface": "s0e2",
					"vlan_id": 10
				}
			]
		}
		self.maxDiff = None
		e = ml_w_vlan.set(None, vlan)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "vlan.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"vconfig": [{"interface": "s0e2", "vlan_id": 10}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['vlan {\n', '    vconfig-array {\n', '        vconfig { #1\n', '            interface s0e2\n', '            vlan_id 10\n', '        }\n', '    }\n', '}\n'])

	def test_vlan_g03(self):
		""" vlan_g03 """
		vlan = {
			"vconfig": [
				{
					"interface": "s0e2",
					"vlan_id": 10
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_vlan.set(None, vlan, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "vlan.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"vconfig": [{"interface": "s0e2", "vlan_id": 10}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['vlan {\n', '    vconfig-array {\n', '        vconfig { #1\n', '            interface s0e2\n', '            vlan_id 10\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
