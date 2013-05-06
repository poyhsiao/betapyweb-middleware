# -*- coding: utf-8 -*1-
import re
#ours
import const
import jcfg
import xt_func
import xtd_logd
from jcfg import N_

RE_FMT="^[\w]{4,255}$"
USER_TABLE="user.json"

def _change_group_in_conf(name, group, conf):
	if name not in conf:
		return (False, [N_("account not found:"), name])

	if group != "admin" and group != "monitor":
		return (False, [N_("invalid group:"), group])

	conf[name]["g"] = group

	return (True, conf)

def _change_group_in_system(name, group, old):
	e = xt_func.sudo(["delgroup", name, old])
	if not e[0]:
		return e

	return xt_func.sudo(["addgroup", name, group])

def _change_password_in_conf(name, password, conf):
	if name not in conf:
		return (False, [N_("account not found:"), name])

	m = re.match(RE_FMT, password)
	if m is None:
		return (False, [N_("invalid password")])

	conf[name]["p"] = password

	return (True, conf)

def _change_password_in_system(name, password):
	return xt_func.sudo(["sh -c 'echo", name+":"+password, "| chpasswd'"])

def _add_account_to_conf(name, param, conf):
	if name in conf:
		return (False, [N_("duplicated name:"), name])

	m = re.match(RE_FMT, name)
	if m is None:
		return (False, [N_("invalid name:"), name])
	
	conf[name] = {}

	e = _change_group_in_conf(name, param["g"], conf)
	if not e[0]:
		return e

	e = _change_password_in_conf(name, param["p"], conf)
	if not e[0]:
		return e

	return (True, conf)

def _add_account_to_system(name, param):
	e = xt_func.sudo(["adduser -DG", param["g"], "-s /swlb/middleware/cli.py", name])
	if not e[0]:
		return e
	
	return _change_password_in_system(name, param["p"])

def _delete_account_in_conf(name, conf):
	if name not in conf:
		return (False, [N_("account not found:"), name])

	if name == "admin" or name == "monitor":
		return (False, [N_("can't delete built-in account:"), name])

	del conf[name]

	return (True, conf)

def _delete_account_in_system(name, group):
	e = xt_func.sudo(["delgroup", name, group])
	if not e[0]:
		return e

	return xt_func.sudo(["deluser", name])

def add_account(name, param, user):
	e = get()
	if not e[0]:
		return e

	e = _add_account_to_conf(name, param, e[1])
	if not e[0]:
		return e
	data = e[1]

	e = _add_account_to_system(name, param)
	if not e[0]:
		return e

	xt_func.save_json(const.CFG_DIR + USER_TABLE, data)

	xtd_logd.add_log(user + " add account: " + name)
	
	return (True, [])

def delete_account(name, user):
	e = get()
	if not e[0]:
		return e

	if name not in e[1]:
		return (False, [N_("account not found:"), name])

	group = e[1][name]["g"]

	e = _delete_account_in_conf(name, e[1])
	if not e[0]:
		return e
	data = e[1]

	e = _delete_account_in_system(name, group)
	if not e[0]:
		return e

	xt_func.save_json(const.CFG_DIR + USER_TABLE, data)
	
	xtd_logd.add_log(user + " delete account: " + name)

	return (True, [])

def change_password(name, password, user):
	e = get()
	if not e[0]:
		return e

	e = _change_password_in_conf(name, password, e[1])
	if not e[0]:
		return e
	data = e[1]

	e = _change_password_in_system(name, password)
	if not e[0]:
		return e

	xt_func.save_json(const.CFG_DIR + USER_TABLE, data)

	xtd_logd.add_log(user + " change password of account: " + name)

	return (True, [])

def change_group(name, group, user):
	e = get()
	if not e[0]:
		return e

	if name not in e[1]:
		return (False, [N_("account not found:"), name])

	old = e[1][name]["g"]
	if old == group:
		return (False, [N_("same group:"), group])

	e = _change_group_in_conf(name, group, e[1])
	if not e[0]:
		return e
	data = e[1]

	e = _change_group_in_system(name, group, old)
	if not e[0]:
		return e

	xt_func.save_json(const.CFG_DIR + USER_TABLE, data)

	xtd_logd.add_log(user+ " change group of account: "+ name+ " to "+ group)

	return (True, [])

def bootup():
	"""For xt_bootup.py"""
	ret = True
	emsg = []
	data = get()[1]
	for account, param in data.iteritems():
		if account == "admin" or account == "monitor":
			e = _change_password_in_system(account, param["p"])
		else:
			e = _add_account_to_system(account, param)
		if not e[0]:
			ret = False
			emsg.append(e[1])
	return (ret, emsg)

def reboot():
	xt_func.reboot("reboot by webUI")
	return (True, [N_("Reboot now")])

def user_default(targets="*", do_reboot=True):
	e = xt_func.sudo(["cp -r", const.MIDWARE_DIR+"factory_default/"+targets, const.CFG_DIR])
	if not e[0]:
		return e
	if do_reboot:
		xt_func.reboot("Reboot now")
		return (True, [N_("Reboot now")])
	return (True, [])
	
def factory_default(targets="*", do_reboot=True):
	e = xt_func.sudo(["cp -r", const.MIDWARE_DIR+"factory_default/"+targets, const.CFG_DIR])
	if not e[0]:
		return e
	if do_reboot:
		xt_func.reboot("Reboot now")
		return (True, [N_("Reboot now")])
	return (True, [])

def firmware_update(updatekey, fwupfile):
	ret = True
	emsg = []
	e = xt_func.sudo(["apply_update ",fwupfile," ",updatekey])
	xt_func.sudo(["rm -rf",fwupfile])
	
	# firmeare update failed return error message
	if not e[0]:
		ret = False
		emsg.append(e[1])
		return (ret, emsg)
	
	#reboot command
	xt_func.reboot("reboot after firmware update")
	return (ret, emsg)

def firmware_downgrade(fwdownfile):
	ret = True
	emsg = []
	e = xt_func.sudo(["apply_downgrade ",fwdownfile])
	xt_func.sudo(["rm -rf",fwdownfile])
	
	# firmeare downgrade failed return error message
	if not e[0]:
		ret = False
		emsg.append(e[1])
		return (ret, emsg)
	
	#reboot command
	xt_func.reboot("reboot after firmware downgrade")
	return (ret, emsg)
	
def importing(imported_file, user):
	ret = True
	emsg = []
	f = open(imported_file, "r")
	lines = f.readlines()
	f.close()
	xt_func.sudo(["rm -rf",imported_file])
	e = jcfg.parse_syntax(lines)
	if not e[0]:
		return e
	data = e[1]
	if "xteralink" not in data:
		return (False, N_("invalid configuration"))
	data = data["xteralink"]
	for i in const.MOD_LIST:
		page = __import__(i)
		if page.TAG not in data:
			print "skip", page.TAG
			continue
		print "importing", page.TAG
		e = jcfg.validate_jcfg(page.HELPER, {page.TAG: data[page.TAG]})
		if not e[0]:
			ret = False
			emsg.append(e[1])
			continue
		e = page.set(e[1][page.TAG], user)
		if not e[0]:
			ret = False
			emsg.append(e[1])
			
	return (ret, emsg)

def export():
	all_exportibles = sorted(const.MOD_LIST)
	rst = "xteralink {\n"
	for i in all_exportibles:
		x = __import__(i)
		e = x.export()[1]
		for j in e:
			rst += " "*4 + j + "\n"
	rst += "}\n"
	return (True, rst)

def get(fname=USER_TABLE, fdir=const.CFG_DIR):
	return xt_func.load_json(fdir+fname)

if __name__ == "__main__":
	import unittest
	class AccountTestCase(unittest.TestCase):
		def test_add_account_to_conf(self):
			data = get("user-g01.json", "unittest/")[1]
			e = _add_account_to_conf("qooq", {"g": "admin", "p": "5567"}, data)
			self.assertEqual(e, (True, {
				"admin": {"g": "admin", "p": "1234"},
				"monitor": {"g": "monitor", "p": "5678"},
				"qooq": {"g": "admin", "p": "5567"},
				}))
		def test_add_same_name(self):
			data = get("user-g01.json", "unittest/")[1]
			e = _add_account_to_conf("admin", {"g": "monitor", "p": "5567"}, data)
			self.assertEqual(e, 
				(False, ["duplicated name:", "admin"]))
		def test_delete_account_in_conf(self):
			data = get("user-g02.json", "unittest/")[1]
			e = _delete_account_in_conf("remove_me", data)
			self.assertEqual(e, (True, {
				"admin": {"g": "admin", "p": "1234"},
				"monitor": {"g": "monitor", "p": "5678"},
				}))
		def test_delete_admin(self):
			data = get("user-g02.json", "unittest/")[1]
			e = _delete_account_in_conf("admin", data)
			self.assertEqual(e, (False, ["can't delete built-in account:", "admin"]))

	suite = unittest.makeSuite(AccountTestCase, "test")
	runner = unittest.TextTestRunner()
	runner.run(suite)

