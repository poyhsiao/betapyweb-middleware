#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - VRRPv2
"""
import unittest
import os
import threading
import ml_w_vrrpv2
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test VRRPv2 """
	def setUp(self):
		""" setUp """

	def test_vrrpv2_g01(self):
		""" vrrpv2_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "vrrpv2-g01.json"), os.path.join("running", "vrrpv2.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "vrrpv2-g01.jcfg"), os.path.join("running", "vrrpv2.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_vrrpv2.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			'group': [
				{
					'group-name': 'VG_1', 
					'instance': [
						{
							'instance-name': 'VI_1',
							'advertisement-interval': 10, 
							'virtual-router-id': 1, 
							'sync-interface': 's0e1', 
							'delay-gratuitous-arp': 5, 
							'priority': 1, 
							'interface': 's0e1', 
							'additional_track_interface': [{'interface': 's0e2'}], 
							'ipv4_vip': [{'interface': 's0e1', 'netmask': '255.255.255.0', 'ipv4': '192.168.1.1'}], 
							'ipv4_vr': [{'interface': 's0e1', 'netmask': '255.255.255.0', 'destination-ipv4': '192.168.1.1', 'gateway': '192.168.1.1'}], 
							'ipv6_vip': [{'interface': 's0e1', 'prefix': 64, 'ipv6': '2001::1'}], 
							'ipv6_vr': [{'interface': 's0e1', 'prefix': 64, 'gateway': '2001::1', 'destination-ipv6': '2001::1'}], 
							'preempt': True
						}
					]
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test VRRPv2 """
	def setUp(self):
		""" setUp """

	def test_vrrpv2_g02(self):
		""" vrrpv2_g02 """
		vrrpv2 = {
			"group": [
				{
					"group-name": "VG_1",
					"instance": [
						{
							"additional_track_interface": [
								{
									"interface": "s0e2"
								}
							],
							"instance-name": "VI_1",
							"interface": "s0e1",
							"sync-interface": "s0e1",
							"delay-gratuitous-arp": 5,
							"virtual-router-id": 1,
							"priority": 1,
							"advertisement-interval": 10,
							"ipv4_vip": [
								{
									"ipv4": "192.168.1.1",
									"netmask": "255.255.255.0",
									"interface": "s0e1"
								}
							],
							"ipv4_vr": [
								{
									"destination-ipv4": "192.168.1.1",
									"netmask": "255.255.255.0",
									"gateway": "192.168.1.1",
									"interface": "s0e1"
								}
							],
							"ipv6_vip": [
								{
									"ipv6": "2001::1",
									"prefix": 64,
									"interface": "s0e1"
								}
							],
							"ipv6_vr": [
								{
									"destination-ipv6": "2001::1",
									"prefix": 64,
									"gateway": "2001::1",
									"interface": "s0e1"
								}
							],
							"preempt": True
						}
					]
				}
			]
		}
		self.maxDiff = None
		e = ml_w_vrrpv2.set(None, vrrpv2)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "vrrpv2.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"group": [{"group-name": "VG_1", "instance": [{"advertisement-interval": 10, "ipv4_vr": [{"interface": "s0e1", "netmask": "255.255.255.0", "destination-ipv4": "192.168.1.1", "gateway": "192.168.1.1"}], "ipv4_vip": [{"interface": "s0e1", "netmask": "255.255.255.0", "ipv4": "192.168.1.1"}], "virtual-router-id": 1, "sync-interface": "s0e1", "delay-gratuitous-arp": 5, "priority": 1, "preempt": true, "ipv6_vip": [{"interface": "s0e1", "prefix": 64, "ipv6": "2001::1"}], "interface": "s0e1", "ipv6_vr": [{"interface": "s0e1", "prefix": 64, "gateway": "2001::1", "destination-ipv6": "2001::1"}], "additional_track_interface": [{"interface": "s0e2"}], "instance-name": "VI_1"}]}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['vrrpv2 {\n', '    group-array {\n', '        group { #1\n', '            group-name VG_1\n', '            instance-array {\n', '                instance { #1\n', '                    instance-name VI_1\n', '                    additional_track_interface-array {\n', '                        additional_track_interface { #1\n', '                        }\n', '                    }\n', '                    delay-gratuitous-arp 5\n', '                    advertisement-interval 10\n', '                    ipv4_vip-array {\n', '                        ipv4_vip { #1\n', '                            ipv4 192.168.1.1\n', '                            netmask 255.255.255.0\n', '                        }\n', '                    }\n', '                    ipv4_vr-array {\n', '                        ipv4_vr { #1\n', '                            destination-ipv4 192.168.1.1\n', '                            netmask 255.255.255.0\n', '                            gateway 192.168.1.1\n', '                        }\n', '                    }\n', '                    ipv6_vip-array {\n', '                        ipv6_vip { #1\n', '                            ipv6 2001::1\n', '                        }\n', '                    }\n', '                    ipv6_vr-array {\n', '                        ipv6_vr { #1\n', '                            destination-ipv6 2001::1\n', '                            gateway 2001::1\n', '                        }\n', '                    }\n', '                }\n', '            }\n', '        }\n', '    }\n', '}\n'])

	def test_vrrpv2_g03(self):
		""" vrrpv2_g03 """
		vrrpv2 = {
			"group": [
				{
					"group-name": "VG_1",
					"instance": [
						{
							"additional_track_interface": [
								{
									"interface": "s0e2"
								}
							],
							"instance-name": "VI_1",
							"interface": "s0e1",
							"sync-interface": "s0e1",
							"delay-gratuitous-arp": 5,
							"virtual-router-id": 1,
							"priority": 1,
							"advertisement-interval": 10,
							"ipv4_vip": [
								{
									"ipv4": "192.168.1.1",
									"netmask": "255.255.255.0",
									"interface": "s0e1"
								}
							],
							"ipv4_vr": [
								{
									"destination-ipv4": "192.168.1.1",
									"netmask": "255.255.255.0",
									"gateway": "192.168.1.1",
									"interface": "s0e1"
								}
							],
							"ipv6_vip": [
								{
									"ipv6": "2001::1",
									"prefix": 64,
									"interface": "s0e1"
								}
							],
							"ipv6_vr": [
								{
									"destination-ipv6": "2001::1",
									"prefix": 64,
									"gateway": "2001::1",
									"interface": "s0e1"
								}
							],
							"preempt": True
						}
					]
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_vrrpv2.set(None, vrrpv2, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "vrrpv2.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"group": [{"group-name": "VG_1", "instance": [{"advertisement-interval": 10, "ipv4_vr": [{"interface": "s0e1", "netmask": "255.255.255.0", "destination-ipv4": "192.168.1.1", "gateway": "192.168.1.1"}], "ipv4_vip": [{"interface": "s0e1", "netmask": "255.255.255.0", "ipv4": "192.168.1.1"}], "virtual-router-id": 1, "sync-interface": "s0e1", "delay-gratuitous-arp": 5, "priority": 1, "preempt": true, "ipv6_vip": [{"interface": "s0e1", "prefix": 64, "ipv6": "2001::1"}], "interface": "s0e1", "ipv6_vr": [{"interface": "s0e1", "prefix": 64, "gateway": "2001::1", "destination-ipv6": "2001::1"}], "additional_track_interface": [{"interface": "s0e2"}], "instance-name": "VI_1"}]}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['vrrpv2 {\n', '    group-array {\n', '        group { #1\n', '            group-name VG_1\n', '            instance-array {\n', '                instance { #1\n', '                    instance-name VI_1\n', '                    additional_track_interface-array {\n', '                        additional_track_interface { #1\n', '                        }\n', '                    }\n', '                    delay-gratuitous-arp 5\n', '                    advertisement-interval 10\n', '                    ipv4_vip-array {\n', '                        ipv4_vip { #1\n', '                            ipv4 192.168.1.1\n', '                            netmask 255.255.255.0\n', '                        }\n', '                    }\n', '                    ipv4_vr-array {\n', '                        ipv4_vr { #1\n', '                            destination-ipv4 192.168.1.1\n', '                            netmask 255.255.255.0\n', '                            gateway 192.168.1.1\n', '                        }\n', '                    }\n', '                    ipv6_vip-array {\n', '                        ipv6_vip { #1\n', '                            ipv6 2001::1\n', '                        }\n', '                    }\n', '                    ipv6_vr-array {\n', '                        ipv6_vr { #1\n', '                            destination-ipv6 2001::1\n', '                            gateway 2001::1\n', '                        }\n', '                    }\n', '                }\n', '            }\n', '        }\n', '    }\n', '}\n'])

	def test_vrrpv2_b04(self):
		""" vrrpv2_b04 """
		vrrpv2 = {
			"group": [
				{
					"group-name": "VG_1",
					"instance": [
						{
							"additional_track_interface": [
								{
									"interface": "s0e2"
								}
							],
							"instance-name": "VI_1",
							"interface": "s0e1",
							"sync-interface": "s0e1",
							"delay-gratuitous-arp": 5,
							"virtual-router-id": 1,
							"priority": 1,
							"advertisement-interval": 10,
							"ipv4_vip": [
								{
									"ipv4": "192.168.1.256",
									"netmask": "255.255.255.0",
									"interface": "s0e1"
								}
							],
							"ipv4_vr": [
								{
									"destination-ipv4": "192.168.1.1",
									"netmask": "255.255.255.0",
									"gateway": "192.168.1.1",
									"interface": "s0e1"
								}
							],
							"ipv6_vip": [
								{
									"ipv6": "2001::1",
									"prefix": 64,
									"interface": "s0e1"
								}
							],
							"ipv6_vr": [
								{
									"destination-ipv6": "2001::1",
									"prefix": 64,
									"gateway": "2001::1",
									"interface": "s0e1"
								}
							],
							"preempt": True
						}
					]
				}
			]
		}
		self.maxDiff = None
		e = ml_w_vrrpv2.set(None, vrrpv2)
		self.assertFalse(e[0], e[1])

if __name__ == "__main__":
	unittest.main()
