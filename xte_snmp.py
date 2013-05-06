# -*- coding: utf-8 -*1-
#ours
import const
import jcfg
import xt_func
from jcfg import N_

TAG="snmp"
STR_HELPER = jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=True)
HELPER = [("snmp", [
	(N_("enable"), jcfg.JcBOOL(default=0)),
	(N_("community"), STR_HELPER),
	(N_("system-name"), STR_HELPER),
	(N_("system-contact"), STR_HELPER),
	(N_("system-location"), STR_HELPER)
])]
DCONF_TMP = "/tmp/snmpd.conf.tmp"
DCONF = "/etc/snmp/snmpd.conf"

#"com2sec Area default [COMMUNITY]"
#"group   Reader  v1      Area"
#"group   Reader  v2c     Area"
#"sysdescr " + const.PRODUCT_NAME
#"syslocation [SYS-LOCATION]"
#"sysname [SYS-NAME]"
#"syscontact [SYS-CONTACT]"
FIXED = [
"view Release included .1.3.6.1.2.1.1.1",
"view Release included .1.3.6.1.2.1.1.2",
"view Release included .1.3.6.1.2.1.1.3",
"view Release included .1.3.6.1.2.1.1.4",
"view Release included .1.3.6.1.2.1.1.5",
"view Release included .1.3.6.1.2.1.1.6",
"view Release included .1.3.6.1.2.1.1.7",
"view Release included .1.3.6.1.2.1.2.2.1.2.2",
"view Release included .1.3.6.1.2.1.2.2.1.2.3",
"view Release included .1.3.6.1.2.1.2.2.1.2.4",
"view Release included .1.3.6.1.2.1.2.2.1.2.5",
"view Release included .1.3.6.1.2.1.2.2.1.2.6",
"view Release included .1.3.6.1.2.1.2.2.1.3.2",
"view Release included .1.3.6.1.2.1.2.2.1.3.3",
"view Release included .1.3.6.1.2.1.2.2.1.3.4",
"view Release included .1.3.6.1.2.1.2.2.1.3.5",
"view Release included .1.3.6.1.2.1.2.2.1.3.6",
"view Release included .1.3.6.1.2.1.2.2.1.5.2",
"view Release included .1.3.6.1.2.1.2.2.1.5.3",
"view Release included .1.3.6.1.2.1.2.2.1.5.4",
"view Release included .1.3.6.1.2.1.2.2.1.5.5",
"view Release included .1.3.6.1.2.1.2.2.1.5.6",
"view Release included .1.3.6.1.2.1.2.2.1.8.2",
"view Release included .1.3.6.1.2.1.2.2.1.8.3",
"view Release included .1.3.6.1.2.1.2.2.1.8.4",
"view Release included .1.3.6.1.2.1.2.2.1.8.5",
"view Release included .1.3.6.1.2.1.2.2.1.8.6",
"view Release included .1.3.6.1.2.1.2.2.1.10.2",
"view Release included .1.3.6.1.2.1.2.2.1.10.3",
"view Release included .1.3.6.1.2.1.2.2.1.10.4",
"view Release included .1.3.6.1.2.1.2.2.1.10.5",
"view Release included .1.3.6.1.2.1.2.2.1.10.6",
"view Release included .1.3.6.1.2.1.2.2.1.11.2",
"view Release included .1.3.6.1.2.1.2.2.1.11.3",
"view Release included .1.3.6.1.2.1.2.2.1.11.4",
"view Release included .1.3.6.1.2.1.2.2.1.11.5",
"view Release included .1.3.6.1.2.1.2.2.1.11.6",
"view Release included .1.3.6.1.2.1.2.2.1.16.2",
"view Release included .1.3.6.1.2.1.2.2.1.16.3",
"view Release included .1.3.6.1.2.1.2.2.1.16.4",
"view Release included .1.3.6.1.2.1.2.2.1.16.5",
"view Release included .1.3.6.1.2.1.2.2.1.16.6",
"view Release included .1.3.6.1.2.1.2.2.1.17.2",
"view Release included .1.3.6.1.2.1.2.2.1.17.3",
"view Release included .1.3.6.1.2.1.2.2.1.17.4",
"view Release included .1.3.6.1.2.1.2.2.1.17.5",
"view Release included .1.3.6.1.2.1.2.2.1.17.6",
"view Release included .1.3.6.1.4.1.2021.10.1.3.1",
"view Release included .1.3.6.1.4.1.2021.10.1.3.2",
"view Release included .1.3.6.1.4.1.2021.10.1.3.3",
'access Reader "" v1  noauth exact Release none none',
'access Reader "" v2c noauth exact Release none none']

def _set(data):
	ret = True
	emsg = []
	xt_func.sudo(["killall snmpd"])
	if data["enable"] == 1: 
		print "RUN"
		f = open(DCONF_TMP, "w")
		f.write("com2sec Area default "+ data["community"]+ "\n");
		f.write("group Reader v1 Area\n");
		f.write("group Reader v2c Area\n");
		f.write("sysdescr "+ const.PRODUCT_NAME+ "\n");
		f.write("syslocation "+ data["system-location"]+ "\n");
		f.write("sysname "+ data["system-name"]+ "\n");
		f.write("syscontact "+ data["system-contact"]+ "\n");
		for l in FIXED:
			f.write(l + "\n");
		f.close()
		e = xt_func.sudo(["mv", DCONF_TMP, DCONF])
		if not e[0]:
			ret = False
			emsg.append(e[1])
		e = xt_func.sudo(["snmpd -c", DCONF])
		if not e[0]:
			ret = False
			emsg.append(e[1])
	return (ret, emsg)
	
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
