# -*- coding: utf-8 -*1-
import json
import copy
import os.path

PRODUCT_NAME="Xteralink"
KILO=1024

CFG_DIR="/swlb/cfg/"

CRON_DIR="/swlb/cron.d/"
CRON_TAB=CRON_DIR+"swlb_crontab"
CRON_SH = {
	"ntpd": CRON_DIR+"ntpd.sh",
	"del_special_accounts": CRON_DIR+"del_special_accounts.sh",
}

MIDWARE_DIR="/swlb/middleware/"

XTCFG_DIR="unittest/"
APPLY_LOCK=XTCFG_DIR+"apply_lock"
IMPORT_LOCK=XTCFG_DIR+"import_lock"

LOG_DIR="/swlb/log/"
FAILURE_LOG=LOG_DIR+"failure.log"
WORKFLOW_LOG=LOG_DIR+"workflow.log"

DAEMON_CFG_DIR=XTCFG_DIR

# platform model eth match while input key and bootup
PLATFORM_MATCH = [
	("1","300",[("eth1", "dmz", "252", "169.254.252.1"),
				("eth2", "lan", "251", "169.254.251.1"),
				("eth0", "wan1", "1", "169.254.1.1"),
				("eth4", "wan2", "2", "169.254.1.2"),
				("eth3", "wan3", "3", "169.254.1.3"),
				("usb1", "wan4", "4", "169.254.1.4")])
]

LICENSE_FILE="license.json"
VERSION_FILE="version.json"

IFMAP = []

try: 
	f = open(CFG_DIR+LICENSE_FILE, "r")
	license_s = json.load(f)
	f.close()
	for i in range(len(PLATFORM_MATCH)):
		if license_s["platform"] == PLATFORM_MATCH[i][0]:
			IFMAP = copy.copy(PLATFORM_MATCH[i][2])
			break
			
except Exception as e:
	pass

ALL_POS = [i[1] for i in IFMAP if not i[0].startswith("usb")]
ALL_USBS = [i[1] for i in IFMAP if i[0].startswith("usb")]
ALL_WANS = [i for i in ALL_POS if i.startswith("wan")]
ALL_NOTWANS = [i for i in ALL_POS if i not in ALL_WANS]
RTAB = dict([[i[1], i[2]] for i in IFMAP if not i[0].startswith("usb")])
DUM_IP = dict([[i[1], i[3]] for i in IFMAP])	

# runtime information. Recreated at bootup
HW_INFO="/var/run/hw_info.json"
BOOTUP_REPORT="/var/run/bootup_report.json"

# daemons
BM_RECORD="/tmp/bmstatd.record"

# configurable modules in the order to executing
MOD_LIST = [
	"xte_network",
	"xte_ip_group",
	"xte_service_group",
	"xte_fqdn",
	"xte_wan_detection",
	"xte_arp_table",
	"xte_auto_routing",
	"xte_connection_limit",
	"xte_dhcp_dmz",
	"xte_dhcp_lan",
	"xte_dns",
	"xte_firewall",
	"xte_nat",
	"xte_snmp",
	"xte_syslog",
	"xte_virtual_server",
	"xte_date_and_time",
	"xte_ddns",
]

