#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Administration (Configuration)
"""
import os
import re
import ml_system
import ml_func

def save_running_to_startup(user = None, threadlock = None):
	"""
		Web UI calls save_running_to_startup()
		return
			(True, None)
			(False, list)
	"""
	status = True
	emsg = []
	e = ml_func.sudo(["rm -rf", ml_system.CFG_STARTUP_PATH])
	if not e[0]:
		status = False
		emsg.append(e[1])
	e = ml_func.sudo(["cp -rf", ml_system.CFG_PATH, ml_system.CFG_STARTUP_PATH])
	if not e[0]:
		status = False
		emsg.append(e[1])
	return (status, emsg)

def save_startup_to_running(user = None, threadlock = None):
	"""
		Web UI calls save_running_to_startup()
		return
			(True, None)
			(False, list)
	"""
	status = True
	emsg = []
	e = ml_func.sudo(["rm -rf", ml_system.CFG_PATH])
	if not e[0]:
		status = False
		emsg.append(e[1])
	e = ml_func.sudo(["cp -rf", ml_system.CFG_STARTUP_PATH, ml_system.CFG_PATH])
	if not e[0]:
		status = False
		emsg.append(e[1])
	return (status, emsg)

def download_running(user = None, threadlock = None):
	"""
		Web UI calls download_running()
		return
			(True, None)
			(False, list)
	"""
	return (True, None)

def download_startup(user = None, threadlock = None):
	"""
		Web UI calls download_startup()
		return
			(True, None)
			(False, list)
	"""
	# backup current running
	# copy startup to running
	# download running
	# delete running
	# restore original running
	return (True, None)

def upload_startup(user = None, threadlock = None):
	"""
		Web UI calls upload_startup()
		return
			(True, None)
			(False, list)
	"""
	# update running and startup???
	return (True, None)
