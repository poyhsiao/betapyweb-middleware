#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - IP Address

	Configuration Data Format
	{
		"ip": [
			{
				"interface": "s0e1",
				"ipv4": [
					{
						"ipv4_address": "192.168.10.1",
						"ipv4_prefix": 24
					},
					...
				],
				"ipv6": [
					{
						"ipv6_address": "2001::1",
						"ipv6_prefix": 64
					},
					...
				]
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_check
import ml_jcfg
from ml_jcfg import N_
import ml_func

class ip_address(ml_config.base):
	""" IP Address """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "ip_address.txt"), threadlock = None):
		""" init config """
		super(ip_address, self).__init__(fpath, threadlock)
		self.tag = "ip_address"
		self.cfg = {}
		self.ipv4_syntax = {
			"ipv4_address": {'T':str, 'D':"192.168.1.1", 'M':True, 'S': None, 'V': [ml_check.validate_ipv4]},
			"ipv4_prefix": {'T':int, 'D':24, 'M':True, 'S': None, 'V': [ml_check.validate_ipv4_prefix]}
		}
		self.ipv4s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv4_syntax}
		}
		self.ipv6_syntax = {
			"ipv6_address": {'T':str, 'D':"2001::1", 'M':True, 'S': None, 'V': [ml_check.validate_ipv6]},
			"ipv6_prefix": {'T':int, 'D':64, 'M':True, 'S': None, 'V': [ml_check.validate_ipv6_prefix]}
		}
		self.ipv6s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv6_syntax}
		}
		self.ip_syntax = {
			"interface": {'T':str, 'D':"s0e1", 'M':True, 'S':None},
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax}
		}
		self.ips_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S':self.ip_syntax},
		}
		self.main_syntax = {
			"ip": {'T':list, 'D':[], 'M':False, 'S':self.ips_syntax}
		}
		self.helper = [(self.tag, [
			(N_("ip"), {
				"[]": [
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1')),
					(N_("ipv4"), {
						"[]": [
							(N_("ipv4_address"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
							(N_("ipv4_prefix"), ml_jcfg.JcINT(default=24))
						]
					}),
					(N_("ipv6"), {
						"[]": [
							(N_("ipv6_address"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
							(N_("ipv6_prefix"), ml_jcfg.JcINT(default=64))
						]
					})
				]
			})
		])]
	def do_set(self):
		""" real task """
		status = True
		emsg = []
		for ip in self.cfg["ip"]:
			ml_func.sudo(["ip link set dev", ip["interface"], "down"])
			ml_func.sudo(["ip addr flush dev", ip["interface"]])
			#ml_func.sudo(["ip route flush table", table])
			#ml_func.sudo(["ip route flush cache"])
			e = ml_func.sudo(["ip link set dev", ip["interface"], "up"])
			if not e[0]:
				status = False
				emsg.append(e[1])
			for ipv4 in ip["ipv4"]:
				e = ml_func.sudo(["ip addr add", ipv4["ipv4_address"] + "/" + str(ipv4["ipv4_prefix"]), "dev", ip["interface"]])
				if not e[0]:
					status = False
					emsg.append(e[1])
			for ipv6 in ip["ipv6"]:
				e = ml_func.sudo(["ip addr add", ipv6["ipv6_address"] + "/" + str(ipv6["ipv6_prefix"]), "dev", ip["interface"]])
				if not e[0]:
					status = False
					emsg.append(e[1])
		if not status:
			return (False, emsg)
		else:
			return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = ip_address(threadlock = threadlock)
		return obj.get()
	except Exception as e:
		return (False, [str(e)])

def set(user = None, cfg = {}, threadlock = None):
	"""
		Web UI calls set()
		return
			(True, None)
			(False, list)
	"""
	try:
		obj = ip_address(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
