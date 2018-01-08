#!/usr/local/bin/python3

import requests
import xml.etree.ElementTree as ET
import shelve
import os, sys

packageListPath = os.environ['PACKAGE_LIST_PATH']
apiUsername = os.environ['CANADA_POST_API_USERNAME']
apiPassword = os.environ['CANADA_POST_API_PASSWORD']
shelfFile = shelve.open(packageListPath)

if 'packages' not in shelfFile:
	shelfFile['packages'] = {}

packages = shelfFile['packages'] 

def getFormattedTime(unformattedTime):
	date = unformattedTime[:4] + "-" + unformattedTime[4:6] + "-" + unformattedTime[6:8]
	time = " " + unformattedTime[9:11] + ":" + unformattedTime[11:13]
	return date + time

def track():
	for pin, description in packages.items():
		print("------------------------------------------------------------------------")
		print(pin + " | " + description) 

		url = "https://soa-gw.canadapost.ca/vis/track/pin/" + pin + "/summary"
		res = requests.get(url, auth=(apiUsername, apiPassword))
		tree = ET.fromstring(res.text)
		pinsummary = tree[0]

		print("Shipped: " + str(pinsummary[5].text))
		print("Expected: " + str(pinsummary[6].text))
		print("Most Recent Update: " + str(pinsummary[10].text) + " in " + str(pinsummary[16].text))
		print("Update Time: " + getFormattedTime(pinsummary[9].text))

	print("------------------------------------------------------------------------" 
		if len(packages) else "No packages | Type 'add [tracking] [description]' to add")

if len(sys.argv) < 2:
	track()
elif sys.argv[1] == "add":
	packages[sys.argv[2]] = " ".join(sys.argv[3:])
elif sys.argv[1] == "remove":
	try:
		del packages[sys.argv[2]]
	except:
		pass

shelfFile['packages'] = packages
shelfFile.close()
