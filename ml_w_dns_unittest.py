#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - DNS
"""
import unittest
import os
import threading
import ml_w_dns
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_dns_g01(self):
		""" dns_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "dns-g01.json"), os.path.join("running", "dns.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "dns-g01.jcfg"), os.path.join("running", "dns.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_dns.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"dns-server-1": "",
			"dns-server-2": "9.8.7.6"
		}))

class test_set(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_dns_g02(self):
		""" dns_g02 """
		dns = {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"dns-server-1": "",
			"dns-server-2": "9.8.7.6"
		}
		self.maxDiff = None
		e = ml_w_dns.set(None, dns)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "dns.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"dns-server-1": "", "dns-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['dns {\n', '    hostname test.host\n', '    domain-name test.domain.org\n', '    dns-server-2 9.8.7.6\n', '}\n'])

	def test_dns_g03(self):
		""" dns_g03 """
		dns = {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"dns-server-1": "",
			"dns-server-2": "9.8.7.6"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_dns.set(None, dns, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "dns.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"dns-server-1": "", "dns-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['dns {\n', '    hostname test.host\n', '    domain-name test.domain.org\n', '    dns-server-2 9.8.7.6\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
