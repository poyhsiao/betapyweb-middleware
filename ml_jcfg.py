#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Config - jcfg
"""
import re
import base64
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

#import const
import ml_func
import ml_system

#import gettext                                            
#localedir = '/swlb/webui/locale/'             
#en_trans = gettext.translation('messages', localedir, languages=['en_US'])
#en_trans.install()

# For deferred translations
def N_(message):
	return message


FIND_ROOT = 0
FIND_KEY = 1
FIND_VALUE = 2
SYNERR_INVAL_VALUE = N_("SYNTAX: invalid value")
SYNERR_MIXED_ARRAY = N_("SYNTAX: mixed-style array")
SYNERR_NO_ARRAY_ITEM = N_("SYNTAX: no array item")
SYNERR_NO_END = N_("SYNTAX: no ending '}'")
SYNERR_NO_KEY = N_("SYNTAX: no valid key")
SYNERR_NO_ROOT = N_("SYNTAX: no root tag")
SYNERR_UNEXP_END = N_("SYNTAX: unexpected '}'")
SEMERR_INVAL_KEY = N_("invalid key")
SEMERR_INVAL_VAL = N_("invalid value")
SEMERR_MUST_ARRAY = N_("mandatory array can't be empty")
SEMERR_MUST_KEY = N_("no mandatory key")
SEMERR_TOO_LESS_ELEM = N_("too less elements")

class JcBase(object):
	def isDefault(self, value):
		return value == self.default

class JcBOOL(JcBase):
	def __init__(self, default=0):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		if data[key] == 0: return (True, 0);
		if data[key] == 1: return (True, 1);
		if data[key] == "True": return (True, True);
		if data[key] == "False": return (True, False);
		return (False, ["Invalid value"])

class JcINT(JcBase):
	def __init__(self, default, min=0, max=65535):
		self.default = default
		self.min = min
		self.max = max
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		try:
			v = int(data[key])
		except:
			return (False, ["Invalid value"])
		if (v == self.default) or ((v >= self.min) and (v <= self.max)):
			return (True, v)
		return (False, ["Invalid value"])

class JcSTR(JcBase):
	def __init__(self, regex, sensitive=False, default=""):
		self.default = default
		self.sensitive = sensitive
		self.regex = regex
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = str(data[key])
		if self.sensitive is False:
			text = text.lower()
		if None is not re.match(self.regex, text): 
			return (True, str(data[key]))
		if text == self.default: 
			return (True, self.default)
		return (False, ["Invalid value"])

class JcAutoRoutingWeight(JcBase):
	def __init__(self):
		# set backward compatibility of config
		self.wan_nums = len(const.ALL_WANS)+len(const.ALL_USBS)
		self.default = ":".join(["1"]*self.wan_nums)
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key]
		m = re.match("^[\d:]+$", text)
		if m is None: 
			return (False, ["Invalid value"])
		tok = text.split(":")
		if len(tok) > self.wan_nums:
			return (False, ["Invalid value"])
		for t in tok:
			v = int(t)
			if (v < 0) or (v > 99): return (False, ["Invalid value"])
		# fill up 0 to wan_nums
		for i in range(self.wan_nums - len(tok)):
			text+=':0'
		return (True, text)

class JcDomainName(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = str(data[key])
		m = re.match(r'^[\w]([\w\-\.]){0,254}$', text)
		if m is None: 
			return (False, ["Invalid value"])
		return (True, text)

class JcFqdn(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key]
		m = re.match("^fqdn@(\d+)$", text)
		if None is not m:
			x = int(m.group(1))
			if str(x) == m.group(1): return (True, text)
		return (False, ["Invalid value"])

class JcGroup(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key]
		m = re.match("^group@(\d+)$", text)
		if None is not m:
			x = int(m.group(1))
			if str(x) == m.group(1): return (True, text)
		return (False, ["Invalid value"])

class JcIpv4(JcBase):
	def __init__(self, default="", a=False, r=False, s=False):
		self.default = default
		self.a = a
		self.r = r
		self.s = s
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		m = re.match("^[\d\.]+(-[\d\.]+)?(/[\d\.]+)?$", data[key])
		if m is None: return (False, ["Invalid value"])
		kind = "a"
		if m.group(1) is not None: kind = "r"
		elif m.group(2) is not None: kind = "s"
		if not getattr(self, kind): return (False, ["Invalid value"])
		if kind == "a":
			if None is ml_func.ip2int(data[key]):
				return (False, ["Invalid value"])
		elif kind == "r":
			tok = data[key].split("-")
			ip1 = ml_func.ip2int(tok[0])
			ip2 = ml_func.ip2int(tok[1])
			if None is ip1 or None is ip2 or ip1 >= ip2: 
				return (False, ["Invalid value"])
		else: #kind == "s"
			tok = data[key].split("/")
			ip = ml_func.ip2int(tok[0])
			mask = ml_func.ip2int(tok[1])
			if None is ip or None is mask or (ip & mask) != ip: 
				return (False, ["Invalid value"])
		return (True, data[key])

class JcIpv4Mask(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		good = ["0.0.0.0",
		    "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0",
		    "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0",
		    "255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0",
		    "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0",
		    "255.255.128.0", "255.255.192.0", "255.255.224.0", "255.255.240.0",
		    "255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0",
		    "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240",
		    "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"]
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		if data[key] in good: return (True, data[key])
		return (False, ["Invalid value"])

class JcL3Proto(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key].lower()
		m = re.match("^proto@(\d+)$", text)
		if None is m: return (False, ["Invalid value"])
		x = int(m.group(1))
		if str(x) != m.group(1) or 0 >= x or x > 0xFF: return (False, ["Invalid value"])
		return (True, text)

class JcL4Proto(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key].lower()
		m = re.match("^(tcp|udp)@(\d+)(-(\d+))?$", text)
		if None is m: return (False, ["Invalid value"])
		x = int(m.group(2))
		if str(x) != m.group(2) or 0 >= x or x > 0xFFFF: return False
		if m.group(4) is not None: 
			y = int(m.group(4))
			if str(y) != m.group(4) or 0 >= y or y > 0xFFFF or y <= x: 
				return (False, ["Invalid value"])
		return (True, text)

class JcMac(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = data[key].lower()
		t = text.split(":")
		if len(t) != 6: return False
		try:
			for i in xrange(0, len(t)):
				v = int(t[i], 16)
				if (i == 0) and (v % 2) != 0:
					return (False, ["Invalid value"])
				if v < 0 or v > 0xFF: 
					return (False, ["Invalid value"])
		except:
			return (False, ["Invalid value"])
		return (True, text)

class JcName(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		text = str(data[key])
		return (True, text)

class JcPassword(JcBase):
	def __init__(self):
		self.default = ""
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		return (True, self.decrypt(data[key]))
	def decrypt(self, text):
		data = base64.b64decode(text)
		i = 0
		n_data = ""
		while i + 3 < len(data):
			n_data += data[i + 3]
			n_data += data[i + 1]
			n_data += data[i + 2]
			n_data += data[i]
			i += 4
		if len(data) < 4:
			n_data = data
		return base64.b64decode(n_data)
	def encrypt(self, val):
		text = str(val)
		data = base64.b64encode(text)
		i = 0
		n_data = ""
		while i + 3 < len(data):
			n_data += data[i + 3]
			n_data += data[i + 1]
			n_data += data[i + 2]
			n_data += data[i]
			i += 4
		if len(data) < 4:
			n_data = data
		return base64.b64encode(n_data)
	def export(self, text):
		return self.encrypt(text)

class JcSelect(JcBase):
	def __init__(self, opt, default=""):
		self.default = default
		self.opt = opt
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		for i in self.opt:
			if isinstance(i, JcBase):
				e = i.validate(data, key)
				if False is not e[0]: 
					return e
			else:
				if i.lower() == data[key].lower(): return (True, i)
		return (False, ["Invalid value"])

class JcTimeString(JcBase):
	def __init__(self, default=""):
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		m = re.match("(\d{0,2}):(\d{0,2})", data[key])
		if None is not m:
			h = int(m.group(1))
			m = int(m.group(2))
			if 0 <= h and h <= 23 and 0 <= m and m <=59:
				return (True, data[key])
		return (False, ["Invalid value"])

class JcTimeZone(JcBase):
	def __init__(self, opt, default=None):
		self.opt = opt
		self.default = default
	def validate(self, data, key):
		if key not in data or data[key] == self.default: 
			return (True, self.default)
		given = data[key].lower()
		for i in self.opt.keys():
			if i.lower() == given:
				return (True, i)
		return (False, ["Invalid value"])

def parse_key(pattern, line):
	m = re.match(pattern, line)
	if m is not None:
		tmpkey = m.group(1)
		line = line[len(tmpkey):].strip()
		return (True, {'ret': tmpkey, "wkl": line})
	return (False, line)

def parse_array_subkey(master, line):
	pattern = r"^(" + master + r")(@\d+)?" # @0 is valid
	ret = {}
	m = re.match(pattern, line)
	if m is not None:
		if m.group(2) is not None:
			ret["ret"] = str(int(m.group(2)[1:]))
		else:
			ret["ret"] = m.group(1)
		ret["wkl"] = line[len(m.group(0)):].strip()
		return (True, ret)
	return (False, line)

def parse_value(pattern, line):
	m = re.match(pattern, line)
	if m is not None:
		try:
			val = int(m.group(1))
			# fix value(leading with zero)change after int() 
			if str(val) != str(m.group(1)):
				val = m.group(1)
		except:
			val = m.group(1)	
		line = line[len(m.group(0)):].strip()
		return (True, {'ret': val, "wkl": line})
	return (False, line)

class SyntaxParser:
	def __init__(self, lines = []):
		self.lines = lines
		self.state = FIND_ROOT
		self.stack = []
	def parse(self, start = 0, remain = None, master = None):
		ln = 0 + start
		tmpkey = ""
		res = {}
		if master is not None:
			res = []
		while len(self.lines) > 0:
			if ln == start and remain is not None:
				wkl = remain.strip()
			else:
				wkl = self.lines[0].strip()
			while len(wkl) > 0:
				if '#' == wkl[0]: break
				if self.state == FIND_ROOT:
					e = parse_key(r"^([\w\-]+)\s*{", wkl)
					if not e[0]:
						return (False, [SYNERR_NO_ROOT, ln + 1])
					self.state = FIND_VALUE
					tmpkey = e[1]['ret']
					wkl = e[1]['wkl']
				elif self.state == FIND_KEY:
					if '}' == wkl[0]:
						if remain is not None: # A child's end
							return (True, {'ret': ln, 'wkl': wkl[1:].strip(), 'res': res})
						return (False, [SYNERR_UNEXP_END, ln + 1])
					if master is not None: # in *-array {
						e = parse_array_subkey(master, wkl)
						if not e[0]: 
							return (False, [
								SYNERR_NO_ARRAY_ITEM, master, ln + 1])
						tmpkey = e[1]['ret']
						wkl = e[1]['wkl']
						self.state = FIND_VALUE
						e = (False, [
							SYNERR_MIXED_ARRAY, ln + 1])
						if tmpkey != master:
							if len(res) == 0:
								res = {}
							elif isinstance(res, list):
								return e
						elif isinstance(res, dict) and len(res) > 0:
							return e
					else:
						m = re.match(r"^([\w\-]*-)?(\w+)-array\s*{", wkl)
						if m is not None:
							wkl = wkl[len(m.group(0)):].strip()
							tmpkey = ""
							if m.group(1) is not None: 
								tmpkey += m.group(1)
							tmpkey += m.group(2)
							e = self.parse(ln, wkl, m.group(2))
							if not e[0]: return e
							ln = e[1]['ret']
							wkl = e[1]['wkl']
							res[tmpkey] = e[1]['res']
							self.state = FIND_KEY
						else:
							e = parse_key(r"^([\w\-]+)", wkl)
							if not e[0]: 
								return (False, [SYNERR_NO_KEY, ln + 1])
							tmpkey = e[1]['ret']
							wkl = e[1]['wkl']
							self.state = FIND_VALUE
				elif self.state == FIND_VALUE:
					child = {}
					if '{' == wkl[0]:
						self.state = FIND_KEY
						e = self.parse(ln, wkl[1:].strip())
						if not e[0]:
							return e
						ln = e[1]['ret']
						wkl = e[1]['wkl']
						child = e[1]['res']
					elif '}' == wkl[0]:
						e = (False, [SYNERR_UNEXP_END, ln + 1])
						return e
					elif '"' == wkl[0]:
						e = parse_value(r'^"([^"]*)"', wkl)
						if not e[0]:
							return (False, [SYNERR_INVAL_VALUE, ln + 1])
						child = e[1]['ret']
						wkl = e[1]['wkl']
					else: 
						e = parse_value(
							r"^(\S+)", wkl)
						if not e[0]:
							return (False, [SYNERR_INVAL_VALUE, ln + 1])
						child = e[1]['ret']
						wkl = e[1]['wkl']
					self.state = FIND_KEY
					if isinstance(res, list):
						res.append(child)
					else:
						res[tmpkey] = child

			ln += 1
			del self.lines[0]
		if remain is not None and self.state == FIND_KEY:
			return (False, [SYNERR_NO_END, ln + 1])
		return (True, res)

def parse_syntax(lines):
	obj = SyntaxParser(lines)
	e = obj.parse()
	#e = obj.parse_new()
	return e

def validate_jcfg(helper, data, array=None, stack=[]):
	#We want to find invalid keys before parsing, so loop twice
	dkeys = data.keys()
	for i in helper:
		if i[0] in dkeys: dkeys.remove(i[0]) 
	if len(dkeys) > 0: return (False, [dkeys[0], SEMERR_INVAL_KEY])

	res = {}
	for (hk, hv) in helper:
		if hk[0] == "_": continue
		if isinstance(hv, list): 	#An object
			if hk not in data: 
				data[hk] = {}
			substack = stack[:]
			substack.append(hk)
			e = validate_jcfg(helper=hv, data=data[hk],
				stack=substack)
			if False is e[0]: return e
			res[hk] = e[1]
		elif isinstance(hv, dict): 	#An array. I know, it is NOT INTUITIVE
			child = []
			substack = stack[:]
			substack.append(hk + "-array")
			min_items = 0
			if hk not in data:
				data[hk] = []
			substack.append(1)
			if isinstance(hv["[]"], JcBase):
				helper = hv["[]"]
				for i in data[hk]:
					tmp = {"_": i}
					e = helper.validate(tmp, "_")
					if e[0]:
						if None is e[1]:
							stack.append(i)
							stack.append(SEMERR_MUST_KEY)
							return (False, stack)
					else:
						substack.append(i)
						substack.append(SEMERR_INVAL_VAL)
						return (False, substack)
					substack[-1] += 1
					child.append(e[1])
			else:
				for i in data[hk]:
					e = validate_jcfg(
						helper=hv["[]"], data=i,
						array=hk, stack=substack)
					if False is e[0]: 
						return e
					substack[-1] += 1
					child.append(e[1])
			res[hk] = child
		else:				#A value
			e = hv.validate(data, hk)
			if e[0]:
				if None is e[1]:
					stack.append(hk)
					stack.append(SEMERR_MUST_KEY)
					return (False, stack)
			else:
				stack.append(hk)
				stack.append(data[hk])
				stack.append(SEMERR_INVAL_VAL)
				return (False, stack)
			res[hk] = e[1]
	return (True, res)

def __to_lines(helper, data, depth=0, array_master=None):
	res = []
	indent = " " * 4 * depth
	for (hk, hv) in helper:
		line = ""
		if hk[0] == "_": continue
		if hk not in data: continue
		line += indent
		k_to_print = hk
		if hk == "[]":
			k_to_print = array_master
		if isinstance(hv, list): #An object
			if len(data[hk]) == 0: continue
			line += "%s {" % k_to_print
			tmp = __to_lines(
				helper=hv, data=data[hk], depth=depth+1)
			if len(tmp) == 0: continue
			res.append(line)
			res.extend(tmp)
			res.append(indent + "}")
		elif isinstance(hv, dict): #An array. I know it is NOT INTUITIVE
			#if len(data[hk]) == 0: continue
			line += "%s-array {" % k_to_print
			tmp = []
			n = 1
			key_to_print = hk
			subkey = None
			m = re.match("^([\w\-]*-)?(\w+)$", hk)
			if m is not None:
				subkey = m.group(2)
			if isinstance(hv["[]"], JcBase):
				subh = [("[]", hv["[]"])]
			else:
				x = [i for i in hv["[]"]]
				subh = [("[]", x)]
			for v in data[hk]:
				subtmp = __to_lines(helper=subh, 
					data={"[]": v}, 
					depth=depth+1, 
					array_master=subkey)
				if len(subtmp) > 0:
					subtmp[0] += " #%d"%(n)
				else:
					#subtmp = ['{0}fqdn "" #{1}'.format(
					#	" "*4*(depth+1), n)]
					subtmp = ['{0}{1} '.format(" "*4*(depth+1), subkey) + '{ ' + '#{0}'.format(n)]
					tmp.extend(subtmp)
					subtmp = ['{0}'.format(" "*4*(depth+1)) + '}']
				tmp.extend(subtmp)
				n += 1
			res.append(line)
			res.extend(tmp)
			res.append(indent + "}")
		else: #A value
			if not hv.isDefault(data[hk]):
				line += str(k_to_print) + " "
				if hasattr(hv, "export"):
					val = hv.export(data[hk])
				else: 
					val = str(data[hk])
				m = re.search("[\s#]", val)
				if m is not None:
					val = '"'+ val+ '"'
				line += val
				if val == "":
					line += '""'
				res.append(line)
	return res

def export_file(helper, fname, fdir):
	e = load_file(helper, fname, fdir)
	if not e[0]:
		return e
	e = __to_lines(helper, e[1])
	if len(e) == 0:
		e = [helper[0][0] + " {}"]
	return (True, e)

def load_file(helper, fname, fdir):
	try: 
		fpath = fdir + fname
		f = open(fpath, "r")
		lines = f.readlines()
		f.close()
	except Exception as e:
		return (False, "jcfg.load_file:" + str(e))
	e = parse_syntax(lines)
	if not e[0]:
		return e
	return validate_jcfg(helper, e[1])

def save_file(helper, data, fname, fdir=ml_system.CFG_PATH):
	fpath = fdir + fname
	lines = __to_lines(helper, data)
	try: 
		f = open(fpath, "w")
		for l in lines:
			f.write(l + "\n")
		f.close()
	except Exception as e:
		return (False, str(e))
	return (True, None)

