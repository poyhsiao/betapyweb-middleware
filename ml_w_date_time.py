#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - DateTime

	Configuration Data Format
	{
		"time_zone": "Taipei",
		"time_server": "59.124.196.83",
		"date": "2013/02/04",
		"time": "13:10:00"
	}

	time_zone value list is in ml_tz.py
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_tz
import ml_func

default = {
	"time_zone": "Taipei",
	"time_server": "59.124.196.83",
	"date": "",
	"time": ""
}

class date_time(ml_config.base):
	""" DateTime """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "date_time.txt"), threadlock = None):
		""" init config """
		super(date_time, self).__init__(fpath, threadlock)
		self.tag = "date_time"
		self.cfg = {}
		self.default = default
		self.main_syntax = {
			"time_zone": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"time_server": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"date": {'T':str, 'D':"", 'M':True, 'S':None}, 
			"time": {'T':str, 'D':"", 'M':True, 'S':None}, 
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("time_zone"), ml_jcfg.JcTimeZone(opt=ml_tz.TZ, default=None)),
			(ml_jcfg.N_("time_server"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True), ml_jcfg.JcDomainName()], default="")),
			(ml_jcfg.N_("date"), ml_jcfg.JcSTR("(\d{0,4})/(\d{0,2})/(\d{0,2})")),
			(ml_jcfg.N_("time"), ml_jcfg.JcTimeString())
		])]
	def do_set(self):
		""" real task """
		f = None
		content = ml_func.sudo(["grep " + self.cfg["time_zone"] + " /usr/share/zoneinfo/zone.tab"])
		if content[0]:
			f = content[1].split()[2]
		else:
			return (False, ["invalid time zone"])
		if f:
			ret = ml_func.sudo(["cp -f /usr/share/zoneinfo/" + f, "/etc/localtime"])
			if not ret[0]:
				return (False, ["set localtime failed"])
		else:
			return (False, ["invalid time zone"])
		if self.cfg["date"] and self.cfg["time"]:
			tb = self.cfg["date"] + " " + self.cfg["time"]
			ret = ml_func.sudo(["date -s ", '\"' + tb + '\"'])
		if self.cfg["time_server"]:
			f = open("/etc/ntp.conf", "w")
			f.writelines("server " + self.cfg["time_server"] + "\n")
			f.close()
			content = ml_func.sudo(["ntpd -qg"])
			if not content[0]:
				return (False, ["fail to start NTP service"])
		e = ml_func.sudo(["hwclock -w"])
		if not e[0]:
			return (False, ["fail to set date_time"])
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = date_time(threadlock = threadlock)
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
		obj = date_time(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
