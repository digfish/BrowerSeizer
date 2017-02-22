#!/usr/bin/env python

import psutil
import os,sys
import subprocess
import webbrowser
import platform
import ConfigParser
import pprint

known_browsers = [
'firefox',
'chrome',
'chromium-browser',
'iexplore',
'safari',
'midori',
'webbrowser-app',
'MicrosoftEdge.exe',
'iexplore.exe'
]

running_on = platform.system()


def win_list_installed_browsers():
	import _winreg as wr
	from collections import OrderedDict

	REG_FILE_LOCATION = "C:\\WINDOWS\\system32\\config\\default"
	PATH_FROM_ROOT =r'SOFTWARE\\Clients\\StartMenuInternet'

	browsers = OrderedDict()
	key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE,PATH_FROM_ROOT)
	reachedKeyEnd = False
	i= 0
	commandline = None
	num_subkeys = wr.QueryInfoKey(key)[0]
	print num_subkeys
	for i in range(0,num_subkeys):
		browser = wr.EnumKey(key,i)
#		print browser
		i+=1
		cmdlineKey = wr.OpenKey(key, browser+"\\shell\\open\\command")
#				wr.CloseKey(key)
		regtuple =  wr.EnumValue(cmdlineKey,0)
		browser_cmdline = regtuple[1]
#		print browser, browser_cmdline
		browsers [ browser ] = browser_cmdline.strip('"')
#		print wr.EnumKey(commandline,0)

#	reg = wr.QueryValue(key,None)
	#reg = R.Registry(open(REG_FILE_LOCATION,"r"))

	return  browsers


def list_installed_browsers():
	if running_on == 'Windows':
		untrimmed_browsers = win_list_installed_browsers()
		# print untrimmed_browsers
		installed_browsers = {}
		for (browser_exec,cmdline) in untrimmed_browsers.iteritems():
			installed_browsers[ browser_exec ] = str(cmdline.split(os.sep)[-1])
		# print installed_browsers
		return installed_browsers
	else:
		installed_browsers = webbrowser._browsers
		return installed_browsers

def get_known_browsers():
	installed_browsers = list_installed_browsers


def search_running_browser():
	running_browsers = dict()

	print "+ + + PROCESSES LIST + + + "

	for pid in psutil.pids():
		p = psutil.Process(pid)

		with p.oneshot():
			try:
				cmdline = p.cmdline()
				execpath = cmdline[0]
				conc_cmdline = " ".join(cmdline)
				#print conc_cmdline.lower()
				found_idsx = []
				for browser_id in known_browsers:
					found_idsx.append(conc_cmdline.lower().find(browser_id.lower()))
				# found_idsx = map(lambda browser_string: conc_cmdline.lower().find(
				# 	browser_string.lower()), known_browsers)
				found_browser_idxs = map(lambda idx: idx >=0,found_idsx)
				browser_idx = None

				try:
					browser_idx = found_browser_idxs.index(True)
				except ValueError:
					continue

				#print "==>>> FOUND! <<<==", found_browser_idxs

				cmdpath_tokens = conc_cmdline.split(os.sep)

				execpath_no_spaces = conc_cmdline.split(' ')[0]

				found_browser = known_browsers[browser_idx]

				#print "found_browser variable:", found_browser

				# if the browser ID is found before the end of the file string, skip it
				#if cmdline_tokens.index(found_browser) != ( len(cmdline_tokens) - 2 ):
				#	continue

				if running_on == 'Linux' :
					running_browsers[ found_browser ] = [execpath_no_spaces]
				else :
					spaced_tokens = conc_cmdline.split(' ')
					browser_path =   ' '.join(spaced_tokens)

					if (spaced_tokens[-1].startswith('http')):
						browser_path = ' '.join(spaced_tokens[:-1])

					running_browsers[ found_browser ] = [  browser_path ]

				print found_browser, '=>', running_browsers[found_browser] #, conc_cmdline

				break

			except Exception as ex:
				continue

	return running_browsers

#			if len(cmdline) > 0 :
#				print pid , " ".join(cmdline)

def read_config():
	homedir = os.getenv('HOME')
	config_path = homedir + os.sep + '.seizer.ini'
	cp = ConfigParser.ConfigParser()
	cp.read([config_path])
#	sections = config.sections()
#	print "config:",cp.sections()
	return cp

def main():
	command = None
	url = None
	config = read_config()

	print "Browsers installed:\n", pprint.pprint(list_installed_browsers())

	print sys.argv

	if len(sys.argv) < 2:
		print "No URLs to open provided ! Exiting!"
		sys.exit(-1)
	else:
		url = sys.argv[1]
		print "URL to open:", url

	running_browsers = search_running_browser()

	print running_browsers
	# if a running browser was found...
	if len (running_browsers) > 0:
		found_browser = running_browsers.keys()[0]
		browser_path = running_browsers[found_browser][0]
		print "Found ", found_browser
		print "Path: ", browser_path
#		print('Do you to open the provided URL with this browser?')
#		answer = raw_input()
#		if answer == 'yes' or answer == '' :
#			webbrowser.register(found_browser)
#			webbrowser.open_new_tab(url)
		command = [browser_path , url]

	else: # if it was not found any running browser, launch one using the selector defined
		print "Couldn't find any suitable browser running..."
		browser_selector_path = None
		try:
			browser_selector_path = config.get('chooser','path')
		except:
			try:
				browser_selector_path = os.environ['SEIZER_CHOOSER']
			except:
				print "Configuration file not found! Getting list of browsers"

		if browser_selector_path is None:
			if running_on == 'Windows' :
				browser_selected = installed_browsers_chooser()
			else:
				browser_selected = installed_browsers_chooser()
				browser_selected = browser_selected.name
			command = [ browser_selected ,  url ]
		else:
			#print "Not found any browser currently running, using the default..."
			print "Using the browser selector to choose the running browser..."
			command = [ browser_selector_path ,  url]

	print "====>" , command
	subprocess.call(command)

def installed_browsers_chooser():
	browsers_list = list_installed_browsers()
	chosen_browser = None
	print browsers_list
	for i in range(1,len(browsers_list)+1):
		print i,browsers_list.keys()[i-1]
	print "Input the number of the browser above and press Enter:"
	option_number = int(raw_input()) - 1

	if running_on == 'Windows':
		chosen_browser_name = browsers_list.keys()[option_number]
		chosen_browser = browsers_list[chosen_browser_name]
		print "Selected ", chosen_browser
	else:
		chosen_browser_name = browsers_list.keys()[option_number]
		chosen_browser = browsers_list[chosen_browser_name][1]
		print "Selected ", chosen_browser.name

	return chosen_browser

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print "Something wrong happened! => ",e
	# print "=> Hit ENTER to close this window !"
	# raw_input()

