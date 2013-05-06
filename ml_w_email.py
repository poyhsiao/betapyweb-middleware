#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Email

	Configuration Data Format
	{
		"alert": True,
		"from": "abc@xtera-ip.com",
		"to": [
			"def@xtera-ip.com"
		],
		"server": "1.2.3.4",
		"timeout": 10
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg

default = {
		"alert": False,
		"from": "",
		"to": [],
		"server": "",
		"timeout": 0
}

class email(ml_config.base):
	""" Email """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "email.txt"), threadlock = None):
		""" init config """
		super(email, self).__init__(fpath, threadlock)
		self.tag = "email"
		self.default = default
		self.to_syntax = {
			"*": {'T': str, 'D': "", 'M': False, 'S':None}
		}
		self.main_syntax = {
			"alert": {'T':bool, 'D':False, 'M':True, 'S':None}, 
			"from": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"to": {'T':list, 'D':[], 'M':True, 'S':self.to_syntax}, 
			"server": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"timeout": {'T':int, 'D':0, 'M':True, 'S':None}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("alert"), ml_jcfg.JcBOOL(default=0)),
			(ml_jcfg.N_("from"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
			(ml_jcfg.N_("to"), {
				"[]": ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)
			}),
			(ml_jcfg.N_("server"), ml_jcfg.JcIpv4(a=True)),
			(ml_jcfg.N_("timeout"), ml_jcfg.JcINT(default=0))
		])]
	def do_set(self):
		""" real task """
		ebuf = ""
		ebuf += "{0}global_defs {{\n".format(" "*0)
		if self.cfg["alert"]:
			ebuf += "{0}notification_email {{\n".format(" "*4)
			for to in self.cfg["to"]:
				ebuf += "{0}%s\n".format(" "*8) % to
			ebuf += "{0}}}\n".format(" "*4)
			ebuf += "{0}notification_email_from %s\n".format(" "*4) % self.cfg["from"]
			ebuf += "{0}smtp_server %s\n".format(" "*4) % self.cfg["server"]
			ebuf += "{0}smtp_connect_timeout %s\n".format(" "*4) % self.cfg["timeout"]
		ebuf += "{0}}}\n".format(" "*0)
		# update conf file
		try:
			file = open("email.conf", "w")
			file.write(ebuf)
			file.close()
		except Exception as e:
			return (False, [str(e)])
		# reload service
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = email(threadlock = threadlock)
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
		obj = email(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
