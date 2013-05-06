#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
"""
keepalived command module
"""
import ml_func

def reload(user = None, threadlock = None):
	"""
		reload keepalived service
		return
			(True, None)
			(False, list)
	"""
	try:
		ml_func.sudo(["cat", "running/email.conf", "running/vrrpv2.conf", "running/slb.conf", "> /etc/keepalived/keepalived.conf"])
		ml_func.sudo(["/etc/rc.d/keepalived restart"])
	except Exception as e:
		return (False, [str(e)])
	return (True, None)
