#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Connection Limit

	Configuration Data Format
	{
		"ipv4": [
			{
				"source_ip": "ANY",
				"destination_ip": "ANY",
				"protocol": "TCP",
				"limit_rate": 5,
				"limit_rate_unit": "second",
				"limit_burst": 5
			},
			{
				"source_ip": "ANY",
				"destination_ip": "ANY",
				"protocol": "UDP",
				"limit_rate": 5,
				"limit_rate_unit": "minute",
				"limit_burst": 5
			},
			...
		],
		"ipv6": [
			{
				"source_ip": "ANY",
				"destination_ip": "ANY",
				"protocol": "TCP",
				"limit_rate": 5,
				"limit_rate_unit": "second",
				"limit_burst": 5
			},
			{
				"source_ip": "ANY",
				"destination_ip": "ANY",
				"protocol": "UDP",
				"limit_rate": 5,
				"limit_rate_unit": "minute",
				"limit_burst": 5
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func
import ml_check

default = {
}

class connection_limit(ml_config.base):
	""" Connection Limit """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "connection_limit.txt"), threadlock = None):
		""" init config """
		super(connection_limit, self).__init__(fpath, threadlock)
		self.tag = "connection_limit"
		self.default = default
		self.ipv4_syntax = {
			"source_ip": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv4, ml_check.validate_NA]},
			"destination_ip": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv4, ml_check.validate_NA]},
			"protocol": {'T':str, 'D':"TCP", 'M':True, 'S':None},
			"limit_rate": {'T':int, 'D':3, 'M':True, 'S': None},
			"limit_rate_unit": {'T':str, 'D':"hour", 'M':True, 'S':None},
			"limit_burst": {'T':int, 'D':5, 'M':True, 'S': None}
		}
		self.ipv6_syntax = {
			"source_ip": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv6, ml_check.validate_NA]},
			"destination_ip": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv6, ml_check.validate_NA]},
			"protocol": {'T':str, 'D':"TCP", 'M':True, 'S':None},
			"limit_rate": {'T':int, 'D':3, 'M':True, 'S': None},
			"limit_rate_unit": {'T':str, 'D':"hour", 'M':True, 'S':None},
			"limit_burst": {'T':int, 'D':5, 'M':True, 'S': None}
		}
		self.ipv4s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv4_syntax}
		}
		self.ipv6s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv6_syntax}
		}
		self.main_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("source_ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), "ANY"])),
					(ml_jcfg.N_("destination_ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), "ANY"])),
					(ml_jcfg.N_("protocol"), ml_jcfg.JcSelect(opt=["TCP", "UDP"])),
					(ml_jcfg.N_("limit_rate"), ml_jcfg.JcINT(default=3)),
					(ml_jcfg.N_("limit_rate_unit"), ml_jcfg.JcSelect(opt=["second", "minute", "hour", "day"])),
					(ml_jcfg.N_("limit_burst"), ml_jcfg.JcINT(default=5))
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("source_ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False), "ANY"])),
					(ml_jcfg.N_("destination_ip"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False), "ANY"])),
					(ml_jcfg.N_("protocol"), ml_jcfg.JcSelect(opt=["TCP", "UDP"])),
					(ml_jcfg.N_("limit_rate"), ml_jcfg.JcINT(default=3)),
					(ml_jcfg.N_("limit_rate_unit"), ml_jcfg.JcSelect(opt=["second", "minute", "hour", "day"])),
					(ml_jcfg.N_("limit_burst"), ml_jcfg.JcINT(default=5))
				]
			})
		])]
	def do_set(self):
		""" real task """
		# clear all connection limit rules
		ml_func.sudo(["iptables -t mangle -F"])
		for cl4 in self.cfg["ipv4"]:
			src = "-s " + cl4["source_ip"]
			dst = "-d " + cl4["destination_ip"]
			protocol = ""
			if "TCP" == cl4["protocol"]:
				protocol = "-p tcp --tcp-flags FIN,SYN,RST,ACK SYN"
			elif "UDP" == cl4["protocol"]:
				protocol = "-p udp"
			else:
				return (False, ["invalid protocol - " + cl4["protocol"]])
			limit = "-m limit "
			if cl4["limit_rate"] >= 0:
				limit += "--limit " + str(cl4["limit_rate"])
				if "day" == cl4["limit_rate_unit"]:
					limit += "/d "
				elif "hour" == cl4["limit_rate_unit"]:
					limit += "/h "
				elif "minute" == cl4["limit_rate_unit"]:
					limit += "/m "
				elif "second" == cl4["limit_rate_unit"]:
					limit += "/s "
				else:
					return (False, ["invalid limit rate unit - " + cl4["limit_rate_unit"]])
			if cl4["limit_burst"] >= 0:
				limit += "--limit-burst " + str(cl4["limit_burst"])
			ret = ml_func.sudo(["iptables -t mangle -A PREROUTING", src, dst, protocol, limit, "-j ACCEPT"])
			if not ret[0]:
				return (False, ["fail to set connection limit rule"])
			ret = ml_func.sudo(["iptables -t mangle -A PREROUTING", src, dst, protocol, "-j DROP"])
			if not ret[0]:
				return (False, ["fail to set connection limit rule"])
		for cl6 in self.cfg["ipv6"]:
			src = "-s " + cl6["source_ip"]
			dst = "-d " + cl6["destination_ip"]
			protocol = ""
			if "TCP" == cl6["protocol"]:
				protocol = "-p tcp --tcp-flags FIN,SYN,RST,ACK SYN"
			elif "UDP" == cl6["protocol"]:
				protocol = "-p udp"
			else:
				return (False, ["invalid protocol - " + cl6["protocol"]])
			limit = "-m limit "
			if cl6["limit_rate"] >= 0:
				limit += "--limit " + str(cl6["limit_rate"])
				if "day" == cl6["limit_rate_unit"]:
					limit += "/d "
				elif "hour" == cl6["limit_rate_unit"]:
					limit += "/h "
				elif "minute" == cl6["limit_rate_unit"]:
					limit += "/m "
				elif "second" == cl6["limit_rate_unit"]:
					limit += "/s "
				else:
					return (False, ["invalid limit rate unit - " + cl6["limit_rate_unit"]])
			if cl6["limit_burst"] >= 0:
				limit += "--limit-burst " + str(cl6["limit_burst"])
			ret = ml_func.sudo(["ip6tables -t mangle -A PREROUTING", src, dst, protocol, limit, "-j ACCEPT"])
			if not ret[0]:
				return (False, ["fail to set connection limit rule"])
			ret = ml_func.sudo(["ip6tables -t mangle -A PREROUTING", src, dst, protocol, "-j DROP"])
			if not ret[0]:
				return (False, ["fail to set connection limit rule"])
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = connection_limit(threadlock = threadlock)
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
		obj = connection_limit(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
