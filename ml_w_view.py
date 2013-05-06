#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - View
"""

def refresh(user = None, threadlock = None):
	"""
		Web UI calls refresh()
		return
			(True, None)
			(False, list)
	"""
	try:
		file = open("/var/log/messages", "r")
		ret = file.readlines()
		file.close()
	except Exception as e:
		return (False, [str(e)])
	return (True, ret)
