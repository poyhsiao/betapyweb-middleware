#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Connection Limit
"""
import unittest
import os
import threading
import shutil
import ml_w_connection_limit
import ml_system

class test_get(unittest.TestCase):
	""" Test Connection Limit """
	def setUp(self):
		""" setUp """

	def test_connection_limit_g01(self):
		""" connection_limit_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "connection_limit-g01.json"), os.path.join("running", "connection_limit.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "connection_limit-g01.jcfg"), os.path.join("running", "connection_limit.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_connection_limit.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"ipv4": [
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			],
			"ipv6": [
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test Connection Limit """
	def setUp(self):
		""" setUp """

	def test_connection_limit_g02(self):
		""" connection_limit_g02 """
		connection_limit = {
			"ipv4": [
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			],
			"ipv6": [
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			]
		}
		self.maxDiff = None
		e = ml_w_connection_limit.set(None, connection_limit)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "connection_limit.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['connection_limit {\n', '    ipv4-array {\n', '        ipv4 { #1\n', '            source_ip 10.10.10.1\n', '            destination_ip 10.10.10.2\n', '            protocol TCP\n', '            limit_rate 5\n', '            limit_rate_unit second\n', '        }\n', '        ipv4 { #2\n', '            source_ip 10.10.10.1\n', '            destination_ip 10.10.10.2\n', '            protocol UDP\n', '            limit_rate 5\n', '            limit_rate_unit minute\n', '        }\n', '    }\n', '    ipv6-array {\n', '        ipv6 { #1\n', '            source_ip 2001::1\n', '            destination_ip 2001::2\n', '            protocol TCP\n', '            limit_rate 5\n', '            limit_rate_unit second\n', '        }\n', '        ipv6 { #2\n', '            source_ip 2001::1\n', '            destination_ip 2001::2\n', '            protocol UDP\n', '            limit_rate 5\n', '            limit_rate_unit minute\n', '        }\n', '    }\n', '}\n'])

	def test_connection_limit_g03(self):
		""" connection_limit_g03 """
		connection_limit = {
			"ipv4": [
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "10.10.10.1",
					"destination_ip": "10.10.10.2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			],
			"ipv6": [
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "TCP",
					"limit_rate": 5,
					"limit_rate_unit": "second",
					"limit_burst": 5
				},
				{
					"source_ip": "2001::1",
					"destination_ip": "2001::2",
					"protocol": "UDP",
					"limit_rate": 5,
					"limit_rate_unit": "minute",
					"limit_burst": 5
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_connection_limit.set(None, connection_limit, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "connection_limit.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"br": [{"STP": true, "name": "s0b1", "hello_time": 5, "interface": ["s0e2"], "max_message_age": 5, "forward_delay": 5}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['connection_limit {\n', '    ipv4-array {\n', '        ipv4 { #1\n', '            source_ip 10.10.10.1\n', '            destination_ip 10.10.10.2\n', '            protocol TCP\n', '            limit_rate 5\n', '            limit_rate_unit second\n', '        }\n', '        ipv4 { #2\n', '            source_ip 10.10.10.1\n', '            destination_ip 10.10.10.2\n', '            protocol UDP\n', '            limit_rate 5\n', '            limit_rate_unit minute\n', '        }\n', '    }\n', '    ipv6-array {\n', '        ipv6 { #1\n', '            source_ip 2001::1\n', '            destination_ip 2001::2\n', '            protocol TCP\n', '            limit_rate 5\n', '            limit_rate_unit second\n', '        }\n', '        ipv6 { #2\n', '            source_ip 2001::1\n', '            destination_ip 2001::2\n', '            protocol UDP\n', '            limit_rate 5\n', '            limit_rate_unit minute\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
