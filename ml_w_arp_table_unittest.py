#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - ARP Table
"""
import unittest
import os
import threading
import ml_w_arp_table
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test ARP Table """
	def setUp(self):
		""" setUp """

	def test_arp_table_g01(self):
		""" arp_table_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "arp_table-g01.json"), os.path.join("running", "arp_table.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "arp_table-g01.jcfg"), os.path.join("running", "arp_table.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_arp_table.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"arp_table-server-1": "",
			"arp_table-server-2": "9.8.7.6"
		}))

class test_set(unittest.TestCase):
	""" Test ARP Table """
	def setUp(self):
		""" setUp """

	def test_arp_table_g02(self):
		""" arp_table_g02 """
		arp_table = {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"arp_table-server-1": "",
			"arp_table-server-2": "9.8.7.6"
		}
		self.maxDiff = None
		e = ml_w_arp_table.set(None, arp_table)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "arp_table.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"arp_table-server-1": "", "arp_table-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['arp_table {\n', '    hostname test.host\n', '    domain-name test.domain.org\n', '    arp_table-server-2 9.8.7.6\n', '}\n'])

	def test_arp_table_g03(self):
		""" arp_table_g03 """
		arp_table = {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"arp_table-server-1": "",
			"arp_table-server-2": "9.8.7.6"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_arp_table.set(None, arp_table, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "arp_table.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"arp_table-server-1": "", "arp_table-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['arp_table {\n', '    hostname test.host\n', '    domain-name test.domain.org\n', '    arp_table-server-2 9.8.7.6\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
