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
import requests


def mac_lookup(mac_addr):
	time.sleep(1.5)
	url = f"http://www.macvendorlookup.com/api/v2/{mac_addr}"
	response = requests.request("GET", url).text
	error_message = f"ERROR: \"{mac_addr}\" is not a valid MAC address!"

	return response if response else "[{\"error_message\":\"ERROR\"}]"

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
	print("\n".join(pad_text(
		{
			"startHex":  "The start of the MAC address range the vendor owns in hexadecimal format",
			"endHex":    "The end of the MAC address range the vendor owns in hexadecimal format",
			"startDec":  "The start of the MAC address range the vendor owns in decimal format",
			"endDec":    "The end of the MAC address range the vendor owns in decimal format",
			"company":   "Company name of the vendor or manufacturer",
			"addressL1": "First line of the address the company provided to IEEE",
			"addressL2": "Second line of the address the company provided to IEEE",
			"addressL3": "Third line of the address the company provided to IEEE",
			"country":   "Country the company is located in",
			"type":      "There are 3 different IEEE databases: oui24, oui36, and iab",
		}
	)))

	clients = read_file("clients.txt")

	for client in clients:
		client = client.split()
		hostname = client[0]
		ip_address = client[1].strip("(").strip(")")
		mac_address = client[3].upper()
		_mac_address = []
		for octet in mac_address.split(":"):
			if len(octet) < 2:
				octet = "0" + octet
			_mac_address.append(octet)
		mac_address = ":".join(_mac_address)

		# print(mac_lookup(mac_address))
		# break

		print()
		print(
			"\n".join(
				pad_text(
					json.loads(mac_lookup(mac_address))[0]
				)
			)
		)


if __name__ == "__main__":
	main()
