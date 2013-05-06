#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Middleware Check
"""
import re
import socket

def unicode2str(input):
	""" Convert unicode to str """
	if isinstance(input, dict):
		return {unicode2str(key): unicode2str(value) for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [unicode2str(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input

def validate_NA(data):
	""" Validate 'NA' """
	return (data == "NA")

def validate_ANY(data):
	""" Validate 'ANY' """
	return (data == "ANY")

def validate_ipv4(data):
	""" Validate IPv4 address """
	if re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z", data):
		for d in data.split("."):
			try:
				if 0 <= int(d) <= 255:
					continue
				else:
					return False
			except Exception as e:
				return False
		return True
	else:
		return False

def validate_ipv4_netmask(data):
	""" Validate IPv4 Netmask """
	if data in [
		"0.0.0.0",
		"128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0",
		"248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0",
		"255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0",
		"255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0",
		"255.255.128.0", "255.255.192.0", "255.255.224.0", "255.255.240.0",
		"255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0",
		"255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240",
		"255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"
	]:
		return True
	else:
		return False

def validate_ipv4_prefix(data):
	""" Validate IPv4 prefix """
	if not isinstance(data, int):
		return False
	if 0 <= data <= 32:
		return True
	else:
		return False

def validate_ipv6(data):
	""" Validate IPv6 address """
	try:
		addr = socket.inet_pton(socket.AF_INET6, data)
	except socket.error: # not a valid address
		return False
	return True

def validate_ipv6_prefix(data):
	""" Validate IPv6 prefix """
	if not isinstance(data, int):
		return False
	if 0 <= data <= 128:
		return True
	else:
		return False

def sync(dst, src, syntax):
	"""
		use src and syntax to synchronize dst
		1. parse src obejct then validate by syntax
		2. copy src to dst
		3. delete null members and add not existing default members with default values
		4. export errors
	"""
	if dst is None or src is None or syntax is None:
		return (False, ["Require valid dst, src, and syntax"])
	# str: copy.
	if isinstance(src, str):
		dst = src
	# int: copy.
	elif isinstance(src, int):
		dst = src
	# bool: copy.
	elif isinstance(src, bool):
		dst = src
	# list: validate and copy.
	elif isinstance(src, list):
		# if src is empty but syntax is mandatory then append default
		if len(src) == 0 and syntax['*']['M']:
			dst.append(syntax['*']['D'])
		else:
			for item in src:
				# jcfg JcBOOL
				if syntax['*']['T'] == bool and item == 1:
					dst.append(True)
				if syntax['*']['T'] == bool and item == 0:
					dst.append(False)
				if isinstance(item, syntax['*']['T']):
					if syntax['*'].has_key('V'):
						v = False
						if len(syntax['*']['V']) == 0:
							v = True
						else:
							for validate in syntax['*']['V']:
								if validate(item):
									v = True
									break
						if not v:
							return (False, ["array-item:" + str(item) + " is invalid"])
					if syntax['*']['T'] == unicode or syntax['*']['T'] == str or syntax['*']['T'] == int or syntax['*']['T'] == bool:
						dst.append(item)
					else:
						tmp = syntax['*']['T']()
						dst.append(tmp)
						e = sync(tmp, item, syntax['*']['S'])
						if not e[0]:
							return e
				elif item is None:
					dst.append(None)
				#else:
				#	return (False, [str(item) + " not match type"])
	# dict: validate and copy.
	elif isinstance(src, dict):
		for key in syntax:
			if src.has_key(key):
				# jcfg JcBOOL
				if syntax[key]['T'] == bool and src[key] == 1:
					dst.update({key:True})
				if syntax[key]['T'] == bool and src[key] == 0:
					dst.update({key:False})
				if isinstance(src[key], syntax[key]['T']):
					if syntax[key].has_key('V'):
						v = False
						if len(syntax[key]['V']) == 0:
							v = True
						else:
							for validate in syntax[key]['V']:
								if validate(src[key]):
									v = True
									break
						if not v:
							return (False, [str(key) + ":" + str(src[key]) + " is invalid"])
					if syntax[key]['T'] == unicode or syntax[key]['T'] == str or syntax[key]['T'] == int or syntax[key]['T'] == bool:
						dst.update({key:src[key]})
					else:
						tmp = syntax[key]['T']()
						dst.update({key:tmp})
						e = sync(tmp, src[key], syntax[key]['S'])
						if not e[0]:
							return e
				elif src[key] is None:
					dst.update({key:None})
				#else:
				#	return (False, [str(src[key]) + " not match type"])
			else:
				if syntax[key]['M']:
					if syntax[key]['T'] == unicode or syntax[key]['T'] == str or syntax[key]['T'] == int or syntax[key]['T'] == bool:
						dst.update({key:syntax[key]['D']})
					else:
						tmp = syntax[key]['D']
						dst.update({key:tmp})
						e = sync(tmp, syntax[key]['T'](), syntax[key]['S'])
						if not e[0]:
							return e
	# tuple: not support.
	elif isinstance(src, tuple):
		return (False, ["Not support tuple"])
	# class: not support.
	elif isinstance(src, object):
		return (False, ["Not support class"])
	else:
		return (False, ["Unknown Type"])
	return (True, None)
