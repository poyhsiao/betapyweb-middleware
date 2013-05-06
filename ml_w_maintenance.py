#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Administration (Maintenance)
"""
import os
import re
import ml_func
import ml_w_configuration

def factory_default(user = None, threadlock = None):
	"""
		Web UI calls factory_default()
		return
			(True, None)
			(False, list)
	"""
	try:
		files = os.listdir(".")
		if files:
			for file in files:
				w = re.match("\Aml_w_\w*?.py\Z", file)
				if w:
					w = re.search("unittest", file)
					if not w:
						mod = __import__(file[:-3], fromlist=[])
						if mod:
							if file[5:-3] in vars(mod):
								obj = getattr(mod, file[5:-3])()
								if obj:
									if hasattr(obj, "factory_default"):
										obj.factory_default()
	except Exception as e:
		return (False, [str(e)])
	ml_w_configuration.save_running_to_startup()
	return (True, None)

def reboot(user = None, threadlock = None):
	"""
		Web UI calls reboot()
		return
			(True, None)
			(False, list)
	"""
	e = ml_func.reboot("reboot by webUI")
	if not e[0]:
		return e
	else:
		return (True, None)
