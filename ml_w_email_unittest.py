#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Email
"""
import unittest
import os
import threading
import ml_w_email
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test Email """
	def setUp(self):
		""" setUp """

	def test_email_g01(self):
		""" email_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "email-g01.json"), os.path.join("running", "email.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "email-g01.jcfg"), os.path.join("running", "email.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_email.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"alert": True,
			"from": "abc@xtera-ip.com",
			"to": ["def@xtera-ip.com"],
			"server": "1.2.3.4",
			"timeout": 10
		}))

class test_set(unittest.TestCase):
	""" Test Email """
	def setUp(self):
		""" setUp """

	def test_email_g02(self):
		""" email_g02 """
		email = {
			"alert": True,
			"from": "abc@xtera-ip.com",
			"to": ["def@xtera-ip.com"],
			"server": "1.2.3.4",
			"timeout": 10
		}
		self.maxDiff = None
		e = ml_w_email.set(None, email)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "email.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"email-server-1": "", "email-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['email {\n', '    alert True\n', '    from abc@xtera-ip.com\n', '    to-array {\n', '        to def@xtera-ip.com #1\n', '    }\n', '    server 1.2.3.4\n', '    timeout 10\n', '}\n'])

	def test_email_g03(self):
		""" email_g03 """
		email = {
			"alert": True,
			"from": "abc@xtera-ip.com",
			"to": ["def@xtera-ip.com"],
			"server": "1.2.3.4",
			"timeout": 10
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_email.set(None, email, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "email.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"email-server-1": "", "email-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['email {\n', '    alert True\n', '    from abc@xtera-ip.com\n', '    to-array {\n', '        to def@xtera-ip.com #1\n', '    }\n', '    server 1.2.3.4\n', '    timeout 10\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
