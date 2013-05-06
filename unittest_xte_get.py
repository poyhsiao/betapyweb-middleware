import unittest
import jcfg

class MyTest(unittest.TestCase):
	def test_ar_g01(self):
		self.maxDiff = None;
		from xte_auto_routing import get
		e = get('ar-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"method": "traffic",
			"parameter": "1:1:1:1",
			"aging": 27,
			"rule": [
				{
				"source": "any",
				"destination": "wan",
				"service": "group@6",
				"wan1": 1,
				"wan2": 1,
				"wan3": 0,
				"wan4": 0,
				"failover": 0,
				"persistent": 1,
				"log": 0}
				]
			}))
	def test_ar_g02(self):
		self.maxDiff = None;
		from xte_auto_routing import get
		e = get('ar-g02.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"method": "weight",
			"parameter": "1:1:1:50",
			"aging": 27,
			"rule": [
				{
				"source": "any",
				"destination": "wan",
				"service": "group@6",
				"wan1": 1,
				"wan2": 1,
				"wan3": 0,
				"wan4": 0,
				"failover": 0,
				"persistent": 1,
				"log": 0}
				]
			}))
	def test_ar_g03(self):
		self.maxDiff = None;
		from xte_auto_routing import get
		e = get('ar-g03.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"method": "weight",
			"parameter": "1:1:1:1",
			"aging": 60,
			"rule": []
			}))
	def test_ar_g04(self):
		self.maxDiff = None;
		from xte_auto_routing import get
		e = get('ar-g04.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"method": "weight",
			"parameter": "1:1:1:1",
			"aging": 60,
			"rule": []
			}))
	def test_ar_b01(self):
		self.maxDiff = None;
		from xte_auto_routing import get
		e = get('ar-b01.txt', 'unittest/');
		self.assertEqual(e, (False, ["xmethod", jcfg.SEMERR_INVAL_KEY]))

	def test_arp_table_g01(self):
		self.maxDiff = None;
		from xte_arp_table import get
		e = get('arp-table-g01.txt', 'unittest/');
		if "dynamic-entry" in e[1]:
			del e[1]["dynamic-entry"]
		self.assertEqual(e, (True, {
			"fixed-entry": [
				{
					"interface": "wan2",
					"ip": "9.9.9.9",
					"mac": "08:00:27:9c:90:55"
				}
			]
			}))
	def test_arp_table_g02(self):
		self.maxDiff = None;
		from xte_arp_table import get
		e = get('arp-table-g02.txt', 'unittest/');
		if "dynamic-entry" in e[1]:
			del e[1]["dynamic-entry"]
		self.assertEqual(e, (True, {"fixed-entry": [
			{
			"interface": "wan2",
			"ip": "9.9.9.9",
			"mac": "08:00:27:9c:90:55"
			},
			{
			"interface": "lan",
			"ip": "9.9.9.11",
			"mac": "08:00:27:9c:90:56"
			}
			]}))
	def test_arp_table_b01(self):
		self.maxDiff = None;
		from xte_arp_table import get
		e = get('arp-table-b01.txt', 'unittest/');
		if "dynamic-entry" in e[1]:
			del e[1]["dynamic-entry"]
		self.assertEqual(e, (False, 
			["SYNTAX: no array item", "entry", 3]))
	def test_arp_table_b02(self):
		self.maxDiff = None;
		from xte_arp_table import get
		e = get('arp-table-b02.txt', 'unittest/');
		if "dynamic-entry" in e[1]:
			del e[1]["dynamic-entry"]
		self.assertEqual(e, (False, 
			["arp-table", "fixed-entry-array", 1, "mac", "09:00:27:9c:90:55", "invalid value"]))

	def test_cl_g01(self):
		self.maxDiff = None;
		from xte_connection_limit import get
		e = get('cl-g01.txt', 'unittest/');
		self.assertEqual(e, 
			(True, {
				"rule": [
					{
					"source": "any",
					"destination": "localhost",
					"rate": 99,
					"service": "any",
					"log": 1}
					]
				}
			)
		)
	def test_cl_b01(self):
		self.maxDiff = None;
		from xte_connection_limit import get
		e = get('cl-b01.txt', 'unittest/');
		self.assertEqual(e, 
			(False, ["connection-limit", "rule-array", 1, "destination", "7.7.7.0/255.255.0.0", jcfg.SEMERR_INVAL_VAL])
		)

	def test_dns_g01(self):
		self.maxDiff = None;
		from xte_dns import get
		e = get('dns-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"hostname": "test.host",
			"domain-name": "test.domain.org",
			"dns-server-1": "",
			"dns-server-2": "9.8.7.6"
			}))

	def test_fqdn_g01(self):
		self.maxDiff = None;
		from xte_fqdn import get
		e = get('fqdn-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"fqdn": [
				"a.b.com",
				"c.d.org",
			]
			}))

	def test_fqdn_g02(self):
		self.maxDiff = None;
		from xte_fqdn import get
		e = get('fqdn-g02.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"fqdn": [
				"a.b.com",
				"",
				"c.d.org",
				"www.104.com"
			]
			}))

	def test_firewall_b01(self):
		self.maxDiff = None;
		from xte_firewall import get
		e = get('fw-b01.txt', 'unittest/');
		self.assertEqual(e, (False, [jcfg.SYNERR_NO_ROOT, 1]))

	def test_firewall_b02(self):
		self.maxDiff = None;
		from xte_firewall import get
		e = get('fw-b02.txt', 'unittest/');
		self.assertEqual(e, (False, [jcfg.SYNERR_NO_END, 9]))

	def test_firewall_b03(self):
		self.maxDiff = None;
		from xte_firewall import get
		e = get('fw-b03.txt', 'unittest/');
		self.assertEqual(e, (False, ["firewall", "rule-array", 1, "action", "denyX", jcfg.SEMERR_INVAL_VAL]))

	def test_firewall_g01(self):
		self.maxDiff = None;
		from xte_firewall import get
		e = get('fw-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"rule": [
				{
				"source": "lan",
				"destination": "any",
				"service": "any",
				"log": 0,
				"action": "deny",
				}
			]
			}))

	def test_ip_group_b01(self):
		self.maxDiff = None;
		from xte_ip_group import get
		e = get('ip-group-b01.txt', 'unittest/');
		self.assertEqual(e, (False, ["ip-group", "group-array", 1, "ip-array", 1, "9.8.7.6-9.8.7.6", jcfg.SEMERR_INVAL_VAL]))
	def test_ip_group_g01(self):
		self.maxDiff = None;
		from xte_ip_group import get
		e = get('ip-group-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"group": [
				{
				"label": "g1",
				"ip": ["9.8.7.6", "5.4.3.0/255.255.255.0"],
				},
				{
				"label": "g2",
				"ip": ["1.2.3.4-1.2.3.100"],
				}
			]
			}))
	def test_ip_group_g02(self):
		self.maxDiff = None;
		from xte_ip_group import get
		e = get('ip-group-g02.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"group": [
				{
				"label": "g1",
				"ip": ["9.8.7.6", "5.4.3.0/255.255.255.0"],
				},
				{
				"label": "",
				"ip": []
				},
				{
				"label": "g3",
				"ip": ["1.2.3.4-1.2.3.100"],
				}

			]
			}))

	def test_nat_g01(self):
		self.diffMax = None
		from xte_nat import get
		e = get('nat-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"wan1": {"enable": 0, "rule": []},
			"wan2": {"enable": 0, "rule": []},
			"wan3": {
				"enable": 0,
				"rule": [ 
					{
					"source": "1.2.3.4",
					"destination": "5.6.7.8",
					"service": "udp@57-69",
					"translate": "9.10.11.12",
					"log": 1
					}
				]
			},
			"wan4": {"enable": 0, "rule": []},
			}))
	def test_nat_g02(self):
		self.maxDiff = None
		from xte_nat import get
		e = get('nat-g02.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"wan1": {
				"enable": 0,
				"rule": [
					{
					"source": "1.2.3.0/255.255.255.0",
					"destination": "group@2",
					"service": "proto@204",
					"translate": "none",
					"log": 0
					},
				]
			},
			"wan2": {"enable": 0, "rule": []},
			"wan3": {
				"enable": 0,
				"rule": [ 
					{
					"source": "fqdn@6",
					"destination": "5.6.7.8-5.6.7.108",
					"service": "udp@57-69",
					"translate": "9.10.11.12",
					"log": 1
					}
				]
			},
			"wan4": {"enable": 0, "rule": []}
			}))

	def test_network_g01(self):
		self.maxDiff = None;
		from xte_network import get
		e = get('network-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"dmz": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "auto"
				},
				"basic-subnet": [],
				"static-route": []
			},
			"lan": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "auto"
				},
				"basic-subnet": [
					{
					"ip": "192.168.0.28",
					"mask": "255.255.255.0"
					},
					{
					"ip": "192.168.0.99-192.168.0.199",
					"mask": "255.255.255.0"
					}
				],
				"static-route": [
					{
					"subnet": "8.8.8.0/255.255.255.0",
					"gateway": "192.168.0.8"
					}
				]
			},
			"wan1": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "100/half"
				},
				"enable": 1,
				"label": "WAN1qq",
				"downstream": 512,
				"upstream": 512,
				"type": "static",
				"static-mode": {
					"ip": [
						"192.168.1.1",
						"192.168.1.50-192.168.1.60"
					],
					"mask": "255.255.255.0",
					"gateway": "192.168.1.254"
				},
				"pppoe-mode": {
					"username": "",
					"password": "",
					"service-name": "",
					"ip": "",
					"daily-redial": ""
				},
				"public-ip-passthrough": {
					"ip": [
						"192.168.1.101",
						"192.168.1.120-192.168.1.127",
					],
					"mask": ""
				}
			},
			"wan2": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "auto",
				},
				"enable": 1,
				"label": "WAN2",
				"downstream": 512,
				"upstream": 512,
				"type": "pppoe",
				"static-mode": {
					"ip": [],
					"mask": "",
					"gateway": "",
				},
				"pppoe-mode": {
					"username": "aaname",
					"password": "_!l=0][<>d ;",
					"service-name": "ssname",
					"ip": "",
					"daily-redial": "05:03"
				},
				"public-ip-passthrough": {"ip": [], "mask": ""}
			},
			"wan3": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "auto",
				},
				"enable": 0,
				"label": "",
				"downstream": 512,
				"upstream": 512,
				"type": "dhcp",
				"static-mode": {
					"mask": "",
					"gateway": "",
					"ip": []
					},
				"pppoe-mode": {
					"username": "",
					"password": "",
					"service-name": "",
					"ip": "",
					"daily-redial": ""
				},
				"public-ip-passthrough": {"ip": [], "mask": ""},
			},
			"wan4": {
				"ethernet": {
					"clone-mac": "",
					"mtu": -1,
					"speed-duplex": "auto",
				},
				"enable": 0,
				"label": "",
				"downstream": 512,
				"upstream": 512,
				"type": "n/a",
				"static-mode": {
					"mask": "",
					"gateway": "",
					"ip": []
					},
				"pppoe-mode": {
					"username": "",
					"password": "",
					"service-name": "",
					"ip": "",
					"daily-redial": ""
				},
				"public-ip-passthrough": {"ip": [], "mask": ""},
			},
			}))

	def test_network_b01(self):
		self.maxDiff = None;
		from xte_network import get
		e = get('network-b01.txt', 'unittest/');
		self.assertEqual(e, 
			(False, ["network", "lan", "basic-subnet-array", 1, "ip", jcfg.SEMERR_MUST_KEY])
		)

	def test_service_group_g01(self):
		self.maxDiff = None;
		from xte_service_group import get
		e = get('service-group-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"group": [
				{
				"label": "g1",
				"service": [
					"proto@27",
					"tcp@6635"
				]},
				{
				"label": "g2",
				"service": [
					"udp@117"
				]}
			]}))

	def test_syslog_g01(self):
		self.maxDiff = None;
		from xte_syslog import get
		e = get('syslog-g01.txt', 'unittest/');
		self.assertEqual(e, 
			(True, {"server": "1.2.3.4", "facility": "local2"}))
	def test_syslog_g02(self):
		self.maxDiff = None;
		from xte_syslog import get
		e = get('syslog-g02.txt', 'unittest/');
		self.assertEqual(e, 
			(True, {"server": "1.2.3.4", "facility": "local0"}))
	def test_syslog_b01(self):
		self.maxDiff = None;
		from xte_syslog import get
		e = get('syslog-b01.txt', 'unittest/');
		self.assertEqual(e, (False, ["syslog", "server", "a.b.c.d", jcfg.SEMERR_INVAL_VAL]))
	def test_syslog_b02(self):
		self.maxDiff = None;
		from xte_syslog import get
		e = get('syslog-b02.txt', 'unittest/');
		self.assertEqual(e, (False, ["syslog", "facility", "loCAL12", jcfg.SEMERR_INVAL_VAL]))

	def test_time_g01(self):
		self.maxDiff = None;
		from xte_date_and_time import get
		e = get('time-g01.txt', 'unittest/');
		del e[1]["date"]
		self.assertEqual(e, (True, {
			"time-zone": "Taipei",
			"time-server": "pool.ntp.org"
			}))
	def test_time_g02(self):
		self.maxDiff = None;
		from xte_date_and_time import get
		e = get('time-g02.txt', 'unittest/');
		del e[1]["date"]
		self.assertEqual(e, (True, {
			"time-zone": "Central Time (USA/Canada)",
			"time-server": ""
			}))

	def test_vs_g01(self):
		self.maxDiff = None;
		from xte_virtual_server import get
		e = get('vs-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"rule": [
				{
				"ip": "7.7.7.7",
				"service": "any",
				"wan1": "none",
				"wan2": "8.8.8.8",
				"wan3": "9.9.9.9",
				"wan4": "none",
				"port-mapping": 0,
				"log": 0}
				]
			}))

	def test_wan_detection_g01(self):
		self.maxDiff = None;
		from xte_wan_detection import get
		e = get('wan-detection-g01.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"ignore-inbound-traffic": 1,
			"wan1": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan3": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [
					{
					"ip": "1.2.3.4",
					"hops": 2
					},
					{
					"ip": "3.4.5.6",
					"hops": 3
					}
				],
				"tcp-target": []
			},
			"wan2": {
				"detection-protocol": "tcp",
				"detection-period": 6,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [
					{
					"ip": "1.2.3.4",
					"port": 26
					},
					{
					"ip": "3.4.5.6",
					"port": 80
					}
				]
			},
			"wan4": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
		}))
	def test_wan_detection_g02(self):
		from xte_wan_detection import get
		self.maxDiff = None;
		e = get('wan-detection-g02.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"ignore-inbound-traffic": 0,
			"wan1": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan2": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan3": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan4": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
		}))
	def test_wan_detection_g03(self):
		from xte_wan_detection import get
		self.maxDiff = None;
		e = get('wan-detection-g03.txt', 'unittest/');
		self.assertEqual(e, (True, {
			"ignore-inbound-traffic": 0,
			"wan1": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan2": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan3": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
			"wan4": {
				"detection-protocol": "icmp",
				"detection-period": 3,
				"targets-per-detection": 0,
				"retries": 1,
				"icmp-target": [],
				"tcp-target": [],
			},
		}))

suite = unittest.makeSuite(MyTest, "test")
runner = unittest.TextTestRunner()
runner.run(suite)
#dhcp-dmz-g01.txt
#dhcp-dmz-g02.txt
#dhcp-dmz-g03.txt
#license-b01.json
#license-g01.json
#snmp-g01.txt
#snmp-g02.txt
