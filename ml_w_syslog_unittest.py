#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Syslog
"""
import unittest
import os
import threading
import ml_w_syslog
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test Syslog """
	def setUp(self):
		""" setUp """

	def test_syslog_g01(self):
		""" syslog_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "syslog-g01.json"), os.path.join("running", "syslog.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "syslog-g01.jcfg"), os.path.join("running", "syslog.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_syslog.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"server_ip": "192.168.0.1",
			"facility": "local0"
		}))

class test_set(unittest.TestCase):
	""" Test Syslog """
	def setUp(self):
		""" setUp """

	def test_syslog_g02(self):
		""" syslog_g02 """
		syslog = {
			"server_ip": "192.168.0.1",
			"facility": "local0"
		}
		self.maxDiff = None
		e = ml_w_syslog.set(None, syslog)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "syslog.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"server_ip": "192.168.0.1", "facility": "local0"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['syslog {\n', '    server_ip 192.168.0.1\n', '}\n'])

	def test_syslog_g03(self):
		""" syslog_g03 """
		syslog = {
			"server_ip": "192.168.0.1",
			"facility": "local0"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_syslog.set(None, syslog, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "syslog.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"server_ip": "192.168.0.1", "facility": "local0"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['syslog {\n', '    server_ip 192.168.0.1\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
