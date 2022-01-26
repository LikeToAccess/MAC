# -*- coding: utf-8 -*-
# filename          : main.py
# description       :
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 01-25-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           :
# py version        : 3.9.10 (must run on 3.6 or higher)
#==============================================================================
import json
import time
from datetime import datetime
import requests
from sheets import Sheets


def mac_lookup(mac_addr):
	time.sleep(1.1)
	url = f"http://www.macvendorlookup.com/api/v2/{mac_addr}"
	response = requests.request("GET", url).text

	return response if response.strip() else "[{\"API-ERROR\":\"Invalid MAC address!\"}]"

def read_file(filename):
	with open(filename, "r") as file:
		lines = file.readlines()

	return lines

def write_file(filename, lines):
	with open(filename, "w") as file:
		file.write(lines)

def pad_text(strings, pad=15):
	response = []
	left_strings, right_strings = strings.keys(), list(strings.values())
	for index, left_string in enumerate(left_strings):
		response.append("{0}:{1}{2}".format(
				left_string, " "*(pad-len(left_string)), right_strings[index]
			)
		)

	return response

def main():
	print("\n"+"\n".join(pad_text(
		{
			"startHex":   "The start of the MAC address range the vendor owns in hexadecimal format",
			"endHex":     "The end of the MAC address range the vendor owns in hexadecimal format",
			"startDec":   "The start of the MAC address range the vendor owns in decimal format",
			"endDec":     "The end of the MAC address range the vendor owns in decimal format",
			"company":    "Company name of the vendor or manufacturer",
			"addressL1":  "First line of the address the company provided to IEEE",
			"addressL2":  "Second line of the address the company provided to IEEE",
			"addressL3":  "Third line of the address the company provided to IEEE",
			"country":    "Country the company is located in",
			"type":       "There are 3 different IEEE databases: oui24, oui36, and iab",
			"macAddress": "The MAC address of the device",
			"hostname":   "Hostname of the device",
			"ipAddress":  "IP address of the device",
			"timeNow":    "Current date and time",
			"count":      "Current number of devices already enumerated",
		}
	)))

	clients = read_file("clients.txt")
	sheets_data = []

	for index, client in enumerate(clients):
		client       = client.split()
		hostname     = client[0]
		ip_address   = client[1].strip("(").strip(")")
		mac_address  = client[3].upper()
		_mac_address = []

		for octet in mac_address.split(":"):
			if len(octet) < 2:
				octet = "0" + octet
			_mac_address.append(octet)
		mac_address = ":".join(_mac_address)

		data = json.loads(mac_lookup(mac_address))[0]
		data["macAddress"] = mac_address
		data["hostname"]   = hostname
		data["ipAddress"]  = ip_address
		data["timeNow"]    = str(datetime.now())
		data["count"]      = index + 1

		sheets_data.append(
			[
				data["count"],                                            # Count
				data["ipAddress"],                                        # IP Address
				"#N/A" if data["hostname"] == "?" else data["hostname"],  # Hostname
				data["macAddress"],                                       # MAC Address
				data["company"] if "company" in data else "#N/A",         # Manufacturer
				data["timeNow"],                                          # Last Updated
			]
		)

		print(
			"\n" + "\n".join(pad_text(data))
		)

		sheets.write(f"Network Devices!B{index+3}:G{len(clients)}", [sheets_data[index]])


if __name__ == "__main__":
	print("Connecting to Google Sheets API...")
	sheets = Sheets("1AnJyw8dHEWilcrac-dYaDIkTMXxxcckcM3K9uw0woLI")  # Google spreadsheet ID
	main()
