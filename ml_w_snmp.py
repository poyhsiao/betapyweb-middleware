#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - SNMP

	Configuration Data Format
	{
		"enable": True,
		"community": "public",
		"system_name": "SLB",
		"system_contact": "info <info@xtera.com>",
		"system_location": "4F, 102 Guangfu S. Road, Daan District, Taipei 10612, Taiwan"
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func

default = {
	"enable": False,
	"community": "public",
	"system_name": "SLB",
	"system_contact": "",
	"system_location": ""
}

class snmp(ml_config.base):
	""" SNMP """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "snmp.txt"), threadlock = None):
		""" init config """
		super(snmp, self).__init__(fpath, threadlock)
		self.tag = "snmp"
		self.default = default
		self.main_syntax = {
			"enable": {'T':bool, 'D':False, 'M':True, 'S':None}, 
			"community": {'T':str, 'D':"public", 'M':True, 'S':None}, 
			"system_name": {'T':str, 'D':"SLB", 'M':True, 'S':None}, 
			"system_contact": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"system_location": {'T':str, 'D':"", 'M':True, 'S':None}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("enable"), ml_jcfg.JcBOOL(default=0)),
			(ml_jcfg.N_("community"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=True)),
			(ml_jcfg.N_("system_name"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=True)),
			(ml_jcfg.N_("system_contact"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=True)),
			(ml_jcfg.N_("system_location"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=True))
		])]
	def do_set(self):
		""" real task """
		ret = True
		emsg = []
		ml_func.sudo(["killall snmpd"])
		if self.cfg["enable"] == 1: 
			f = open("/tmp/snmpd.conf", "w")
			f.write("rocommunity "+ self.cfg["community"]+ "\n");
			f.write("rwcommunity "+ self.cfg["community"]+ "\n");
			f.write("sysLocation "+ self.cfg["system_location"]+ "\n");
			f.write("sysName "+ self.cfg["system_name"]+ "\n");
			f.write("sysDescr "+ self.cfg["system_name"]+ "\n");
			f.write("sysContact "+ self.cfg["system_contact"]+ "\n");
			f.close()
			e = ml_func.sudo(["mv", "/tmp/snmpd.conf", "/etc/snmp/snmpd.conf"])
			if not e[0]:
				ret = False
				emsg.append(e[1])
			e = ml_func.sudo(["snmpd -c", "/etc/snmp/snmpd.conf"])
			if not e[0]:
				ret = False
				emsg.append(e[1])
		if not ret:
			return (False, emsg)
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = snmp(threadlock = threadlock)
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
		obj = snmp(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
