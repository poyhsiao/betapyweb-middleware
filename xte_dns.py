import datetime
#ours
import const
import jcfg
import xt_func
from jcfg import N_

TAG = "dns"
HELPER = [("dns", [
	(N_("hostname"), jcfg.JcDomainName()),
	(N_("domain-name"), jcfg.JcDomainName()),
	(N_("dns-server-1"), jcfg.JcIpv4(a=True)),
	(N_("dns-server-2"), jcfg.JcIpv4(a=True))
])]

def _set(data):
	f = open("/tmp/hostname", "w")
	f.write(data["hostname"])
	f.close()

	f = open("/tmp/resolv.conf", "w")
	f.write("#"+ str(datetime.datetime.now()) + "\n")
	if data["domain-name"] != "":
		f.write("search " + data["domain-name"] + "\n")
	if data["dns-server-1"] != "": 
		f.write("nameserver " + data["dns-server-1"]+ "\n")
	if data["dns-server-2"] != "": 
		f.write("nameserver " + data["dns-server-2"]+ "\n")
	f.close()

	ret = True
	e = xt_func.sudo(["hostname", str(data["hostname"])])
	if not e[0]: ret = False
	e = xt_func.sudo(["mv /tmp/hostname /etc/"])
	if not e[0]: ret = False
	e = xt_func.sudo(["mv /tmp/resolv.conf /etc/"])
	if not e[0]: ret = False
	return (ret, None)

def export(fname=TAG+".txt", fdir=const.CFG_DIR):
	return jcfg.export_file(HELPER, fname, fdir)

def get(fname=TAG+".txt", fdir=const.CFG_DIR):
	return xt_func.xte_get(TAG, HELPER, fname, fdir)

def importing(fname=TAG+".txt", fdir=const.CFG_DIR):
	return (True, None)

def set(data, user, fname=TAG+".txt", fdir=const.CFG_DIR):
	e = validate(data)
	if e[0]:
		e = xt_func.xte_set(TAG, HELPER, data, _set, fname, fdir, user)
	return e

def validate(data):
	return jcfg.validate_jcfg(HELPER, {TAG: data})
