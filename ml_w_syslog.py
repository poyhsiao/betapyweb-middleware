#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Syslog

	Configuration Data Format
	{
		"server_ip": "192.168.0.1",
		"facility": "local0"
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func

default = {
	"server_ip": "127.0.0.1",
	"facility": "local0"
}
facility_list = ["local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"]

class syslog(ml_config.base):
	""" Syslog """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "syslog.txt"), threadlock = None):
		""" init config """
		super(syslog, self).__init__(fpath, threadlock)
		self.tag = "syslog"
		self.default = default
		self.main_syntax = {
			"server_ip": {'T':str, 'D':"127.0.0.1", 'M':True, 'S':None}, 
			"facility": {'T':str, 'D':"local0", 'M':True, 'S':None}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("server_ip"), ml_jcfg.JcIpv4(a=True)),
			(ml_jcfg.N_("facility"), ml_jcfg.JcSelect(opt=facility_list, default="local0"))
		])]
	def do_set(self):
		""" real task """
		status = True
		emsg = []
		for f in facility_list:
			e = ml_func.sudo(["sed -i '/" + f + "/d' /etc/rsyslog.conf"])
		e = ml_func.sudo(["echo '" + self.cfg["facility"] + "\t\t@" + self.cfg["server_ip"] + "' >> /etc/rsyslog.conf"])
		e = ml_func.sudo(["/etc/rc.d/rsyslogd restart"])
		if not e[0]:
			status = False
			emsg.append(e[1])
		if not status:
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
		obj = syslog(threadlock = threadlock)
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
		obj = syslog(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
