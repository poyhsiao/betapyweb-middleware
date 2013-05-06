#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - SNMP
"""
import unittest
import os
import threading
import ml_w_snmp
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test SNMP """
	def setUp(self):
		""" setUp """

	def test_snmp_g01(self):
		""" snmp_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "snmp-g01.json"), os.path.join("running", "snmp.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "snmp-g01.jcfg"), os.path.join("running", "snmp.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_snmp.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"enable": True,
			"community": "public",
			"system_name": "SLB",
			"system_contact": "info <info@xtera.com>",
			"system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"
		}))

class test_set(unittest.TestCase):
	""" Test SNMP """
	def setUp(self):
		""" setUp """

	def test_snmp_g02(self):
		""" snmp_g02 """
		snmp = {
			"enable": True,
			"community": "public",
			"system_name": "SLB",
			"system_contact": "info <info@xtera.com>",
			"system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"
		}
		self.maxDiff = None
		e = ml_w_snmp.set(None, snmp)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "snmp.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"system_name": "SLB", "system_contact": "info <info@xtera.com>", "enable": true, "system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan", "community": "public"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['snmp {\n', '    enable True\n', '    community public\n', '    system_name SLB\n', '    system_contact "info <info@xtera.com>"\n', '    system_location "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"\n', '}\n'])

	def test_snmp_g03(self):
		""" snmp_g03 """
		snmp = {
			"enable": True,
			"community": "public",
			"system_name": "SLB",
			"system_contact": "info <info@xtera.com>",
			"system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_snmp.set(None, snmp, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "snmp.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"system_name": "SLB", "system_contact": "info <info@xtera.com>", "enable": true, "system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan", "community": "public"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['snmp {\n', '    enable True\n', '    community public\n', '    system_name SLB\n', '    system_contact "info <info@xtera.com>"\n', '    system_location "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
