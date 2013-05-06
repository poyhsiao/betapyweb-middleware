#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - NAT64

	Configuration Data Format
	{
		"enable": True,
		"ipv6": "64:ff9b::",
		"ipv6_prefix": 96,
		"ipv4": "0.0.0.0"
	}
"""
import os
import stat
import ml_system
import ml_config
import ml_jcfg
import ml_check
import ml_func

default = {
	"enable": False,
	"ipv6": "64:ff9b::",
	"ipv6_prefix": 96,
	"ipv4": "0.0.0.0"
}

class nat64(ml_config.base):
	""" NAT64 """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "nat64.txt"), threadlock = None):
		""" init config """
		super(nat64, self).__init__(fpath, threadlock)
		self.tag = "nat64"
		self.default = default
		self.main_syntax = {
			"enable": {'T':bool, 'D':False, 'M':True, 'S':None},
			"ipv6": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv6]},
			"ipv6_prefix": {'T':int, 'D':96, 'M':True, 'S': None},
			"ipv4": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv4]}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("enable"), ml_jcfg.JcBOOL(default=0)),
			(ml_jcfg.N_("ipv6"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="64:ff9b::", sensitive=False)),
			(ml_jcfg.N_("ipv6_prefix"), ml_jcfg.JcINT(default=96)),
			(ml_jcfg.N_("ipv4"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0"))
		])]
	def do_set(self):
		""" real task """
		# please install ecdysis
		if self.cfg["enable"]:
			ret = ml_func.sudo(["cp -f nat64-config.sample nat64-config.sh"])
			if "0.0.0.0" != self.cfg["ipv4"]:
				ret = ml_func.sudo(["sed -i 's/#IPV4_ADDR/IPV4_ADDR/' nat64-config.sh"])
				ret = ml_func.sudo(["sed -i 's/XTERA-IPV4/" + self.cfg["ipv4"] + "/' nat64-config.sh"])
			ret = ml_func.sudo(["sed -i 's/XTERA-IPV6/" + self.cfg["ipv6"] + "/' nat64-config.sh"])
			ret = ml_func.sudo(["sed -i 's/XTERA-PREFIX/" + str(self.cfg["ipv6_prefix"]) + "/' nat64-config.sh"])
			ret = ml_func.sudo(["mv -f nat64-config.sh /bin"])
			if not ret[0]:
				return (False, ["fail to parse nat64 script"])
			try:
				os.chmod("/bin/nat64-config.sh",
					stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
					stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
				)
			except Exception as e:
				return (False, [str(e)])
			ml_func.sudo(["nat64-config.sh"])
		else:
			ml_func.sudo(["ifconfig nat64 down"])
			ml_func.sudo(["rmmod nf_nat64"])
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = nat64(threadlock = threadlock)
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
		obj = nat64(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
