#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - ARP Table

	Configuration Data Format
	{
		"ipv4_static": [
			{
				"interface":"s0e1",
				"ip":"192.168.0.135",
				"mac":"08:00:27:fd:9d:f9"
			},
			...
		],
		"ipv4_dynamic": [
			{
				"interface":"s0e1",
				"ip":"192.168.0.112",
				"mac":"6c:f0:27:fd:ea:23"
			},
			...
		],
		"ipv6_static": [
			{
				"interface":"s0e1",
				"ip":"2001::1234",
				"mac":"08:00:27:fd:9d:f9"
			},
			...
		],
		"ipv6_dynamic": [
			{
				"interface":"s0e1",
				"ip":"2001::2468",
				"mac":"6c:f0:27:fd:ea:23"
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
from ml_jcfg import N_
import ml_check
import ml_func
import re

class arp_table(ml_config.base):
	""" ARP Table """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "arp_table.txt"), threadlock = None):
		""" init config """
		super(arp_table, self).__init__(fpath, threadlock)
		self.tag = "arp_table"
		self.cfg = {}
		self.ipv4_syntax = {
			"interface": {'T':str, 'D':"s0e1", 'M':True, 'S':None},
			"ip": {'T':str, 'D':"192.168.1.1", 'M':True, 'S':None, 'V':[ml_check.validate_ipv4]},
			"mac": {'T':str, 'D':"00:00:00:00:00:00", 'M':True, 'S':None}
		}
		self.ipv6_syntax = {
			"interface": {'T':str, 'D':"s0e1", 'M':True, 'S':None},
			"ip": {'T':str, 'D':"2001::1234", 'M':True, 'S':None, 'V':[ml_check.validate_ipv6]},
			"mac": {'T':str, 'D':"00:00:00:00:00:00", 'M':True, 'S':None}
		}
		self.ipv4s_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S':self.ipv4_syntax}
		}
		self.ipv6s_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S':self.ipv6_syntax}
		}
		self.main_syntax = {
			"ipv4_static": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv4_dynamic": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv6_static": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax},
			"ipv6_dynamic": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax}
		}
		self.helper = [(self.tag, [
			(N_("ipv4_static"), {
				"[]": [
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')),
					(N_("ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
					(N_("mac"), ml_jcfg.JcMac())
				]
			}),
			(N_("ipv4_dynamic"), {
				"[]": [
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')),
					(N_("ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
					(N_("mac"), ml_jcfg.JcMac())
				]
			}),
			(N_("ipv6_static"), {
				"[]": [
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')),
					(N_("ip"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
					(N_("mac"), ml_jcfg.JcMac())
				]
			}),
			(N_("ipv6_dynamic"), {
				"[]": [
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')),
					(N_("ip"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
					(N_("mac"), ml_jcfg.JcMac())
				]
			})
		])]
	def do_get(self):
		""" real task """
		content = ml_func.sudo(["arp -an", "| grep -v PERM", "| grep -v incomplete"])
		if content[0]:
			lines = content[1].split("\n")
			for line in lines:
				i = re.search("\(.*\)", line)
				m = re.search("at .*? ", line)
				d = re.search("on .*", line)
				if i and m and d:
					self.cfg["ipv4_dynamic"].append({
						"interface":line[d.start()+3:d.end()],
						"ip":line[i.start()+1:i.end()-1],
						"mac":line[m.start()+3:m.end()-1]
					})
		content = ml_func.sudo(["ip -6 neigh show", "| grep -v PERMANENT", "| grep -v INCOMPLETE"])
		if content[0]:
			lines = content[1].split("\n")
			for line in lines:
				i = re.search("\A.*? ", line)
				m = re.search("lladdr .*? ", line)
				d = re.search("dev .*? ", line)
				if i and m and d:
					self.cfg["ipv6_dynamic"].append({
						"interface":line[d.start()+4:d.end()-1],
						"ip":line[i.start():i.end()-1],
						"mac":line[m.start()+7:m.end()-1]
					})
		return (True, None)
	def do_set(self):
		""" real task """
		status = True
		emsg = []

		content = ml_func.sudo(["arp -an", "| grep PERM"])
		if content[0]:
			lines = content[1].split("\n")
			for line in lines:
				m = re.search("\(.*\)", line)
				if m:
					ret = ml_func.sudo(["arp -d ", line[m.start()+1:m.end()-1]])
					if not ret[0]:
						return ret
		for ipv4 in self.cfg["ipv4_static"]:
			ret = ml_func.sudo(["arp -i", ipv4["interface"], "-s", ipv4["ip"], ipv4["mac"]])
			if not ret[0]:
				status = False
				emsg.append(ret[1])
		del self.cfg["ipv4_dynamic"][:]
		content = ml_func.sudo(["ip -6 neigh show", "| grep PERMANENT"])
		if content[0]:
			lines = content[1].split("\n")
			for line in lines:
				if len(line.split()) >= 3:
					ret = ml_func.sudo(["ip -6 neigh del", line.split()[0], "dev", line.split()[2]])
					if not ret[0]:
						return ret
		for ipv6 in self.cfg["ipv6_static"]:
			ret = ml_func.sudo(["ip -6 neigh add", ipv6["ip"], "lladdr", ipv6["mac"], "dev", ipv6["interface"]])
			#if not ret[0]:
			#	status = False
			#	emsg.append(ret[1])
		del self.cfg["ipv6_dynamic"][:]

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
		obj = arp_table(threadlock = threadlock)
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
		obj = arp_table(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
