#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - CLI
"""
import unittest
import os
import threading
import ml_w_cli
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test CLI """
	def setUp(self):
		""" setUp """

	def test_cli_g01(self):
		""" cli_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "cli-g01.json"), os.path.join("running", "cli.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "cli-g01.jcfg"), os.path.join("running", "cli.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_cli.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"ssh": True,
			"telnet": False
		}))

class test_set(unittest.TestCase):
	""" Test CLI """
	def setUp(self):
		""" setUp """

	def test_cli_g02(self):
		""" cli_g02 """
		cli = {
			"ssh": True,
			"telnet": False
		}
		self.maxDiff = None
		e = ml_w_cli.set(None, cli)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "cli.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ssh": true, "telnet": false}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, [])

	def test_cli_g03(self):
		""" cli_g03 """
		cli = {
			"ssh": True,
			"telnet": False
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_cli.set(None, cli, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "cli.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ssh": true, "telnet": false}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, [])

if __name__ == "__main__":
	unittest.main()
