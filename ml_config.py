#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Config
"""
import os
import ml_log
import ml_jcfg
import pickle
import json
import ml_system
import fcntl
import ml_check

class config(object):
	""" Configuration file base class """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "config.txt"), threadlock = None):
		""" init config """
		self.tag = "config"
		ml_log.log(self.tag + ".__init__")
		self.fpath = fpath
		self.cfg = {}
		self.default = {}
		self.main_syntax = {}
		self.helper = []
		# lock
		self.lockfile = None
		self.threadlock = threadlock
	def load(self):
		""" load from a file """
		ml_log.log(self.tag + ".load()")
		self.read_lock()
		e = self.do_load()
		self.read_unlock()
		if not e[0]:
			return e

		ret = ml_check.sync(self.cfg, e[1], self.main_syntax)
		if not ret[0]:
			return ret

		return (True, None)
	def do_load(self):
		""" load from a file """
		return (True, {})
	def dump(self):
		""" dump to a file """
		ml_log.log(self.tag + ".dump()")

		# ignore empty config items (None or "") maybe include default
		dumpcfg = {}
		dumpcfg.update(self.cfg)
		#for k in dumpcfg.keys():
		#	if not dumpcfg[k] or dumpcfg[k] == "":
		#		dumpcfg.pop(k)

		self.write_lock()
		ret = self.do_dump(dumpcfg)
		self.write_unlock()
		return ret
	def do_dump(self, cfg={}):
		""" dump to a file """
		return (True, None)
	def get(self):
		""" load, do_get. """
		ml_log.log(self.tag + ".get()")
		e = self.load()
		if not e[0]:
			return e
		self.write_lock()
		try:
			ret = self.do_get()
		except Exception as e:
			ret = (False, [str(e)])
		self.write_unlock()
		if not ret[0]:
			return ret
		return (True, self.cfg.copy())
	def do_get(self):
		""" real task """
		return (True, None)
	def set(self, cfg={}):
		""" sync config, do_set, dump. """
		ml_log.log(self.tag + ".set()")

		ret = ml_check.sync(self.cfg, cfg, self.main_syntax)
		if not ret[0]:
			return ret

		self.write_lock()
		try:
			ret = self.do_set()
		except Exception as e:
			ret = (False, [str(e)])
		self.write_unlock()
		if not ret[0]:
			# do_set fails, load old cfg then do_set.
			ret_load = self.load()
			if ret_load[0]:
				self.write_lock()
				try:
					ret_set = self.do_set()
				except Exception as e:
					ret_set = (False, [str(e)])
				self.write_unlock()
			return ret
		else:
			return self.dump()
	def do_set(self):
		""" real task """
		return (True, None)
	def read_lock(self):
		""" enter critical section """
		ml_log.log(self.tag + ".read_lock")
		self.lockfile = open(ml_system.LOCK_FILE, "w")
		fcntl.flock(self.lockfile, fcntl.LOCK_SH)
		if self.threadlock:
			self.threadlock.acquire()
	def read_unlock(self):
		""" leave critical section """
		ml_log.log(self.tag + ".read_unlock")
		self.unlock()
	def write_lock(self):
		""" enter critical section """
		ml_log.log(self.tag + ".write_lock")
		self.lockfile = open(ml_system.LOCK_FILE, "w")
		fcntl.flock(self.lockfile, fcntl.LOCK_EX)
		if self.threadlock:
			self.threadlock.acquire()
	def write_unlock(self):
		""" leave critical section """
		ml_log.log(self.tag + ".write_unlock")
		self.unlock()
	def unlock(self):
		""" leave critical section """
		if self.threadlock:
			self.threadlock.release()
		fcntl.flock(self.lockfile, fcntl.LOCK_UN)
		self.lockfile.close()
	def factory_default(self):
		""" factory default """
		return self.set(self.default)

class jcfg_config(config):
	""" Xtera config format """
	def do_load(self):
		""" load from a file """
		e = ml_jcfg.load_file(self.helper, self.fpath, "")
		if not e[0]:
			return e
		cfg = e[1][self.tag]
		return (True, cfg)
	def do_dump(self, cfg={}):
		""" dump to a file """
		emsg = []
		e = ml_jcfg.save_file(self.helper, {self.tag: cfg}, self.fpath, "")
		if not e[0]:
			emsg.append(e[1])
			return (False, emsg)
		return (True, None)

class pickle_config(config):
	""" pickle format """
	def do_load(self):
		""" load from a file """
		try:
			self.file = open(self.fpath, "r")
			cfg = pickle.load(self.file)
			self.file.close()
		except Exception as e:
			return (False, [str(e)])
		return (True, cfg)
	def do_dump(self, cfg={}):
		""" dump to a file """
		try:
			self.file = open(self.fpath, "w")
			pickle.dump(cfg, self.file)
			self.file.close()
		except Exception as e:
			return (False, [str(e)])
		return (True, None)

class json_config(config):
	""" json format """
	def do_load(self):
		""" load from a file """
		try:
			self.file = open(self.fpath, "r")
			cfg = json.load(self.file)
			self.file.close()
		except Exception as e:
			return (False, [str(e)])
		cfg = ml_check.unicode2str(cfg)
		return (True, cfg)
	def do_dump(self, cfg={}):
		""" dump to a file """
		try:
			self.file = open(self.fpath, "w")
			json.dump(cfg, self.file)
			self.file.close()
		except Exception as e:
			return (False, [str(e)])
		return (True, None)

if "jcfg" == ml_system.CFG_TYPE:
	base = jcfg_config
elif "json" == ml_system.CFG_TYPE:
	base = json_config
elif "pickle" == ml_system.CFG_TYPE:
	base = pickle_config
else:
	base = json_config

def import_config():
	""" import config from file """

def export_config():
	""" export config to file """
