# -*- coding: utf-8 -*-

def execute(command, ret = True):
  	'''function to exec everything, subprocess used to fork'''
		
	if ret == True :
		p = os.popen(command)
		return p.readline()
		p.close
	else:
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#explictly use subprocess
def executep(command, ret = True):
  	'''function to exec everything, subprocess used to fork'''
		
	if ret == True :
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)



def functions(view, frame, req, data=None):
	
	'''base functions'''
	uri = req.get_uri()
	lllink, path=uri.split('://', 1)
	path = path.replace("%20"," ")
	print lllink
	print uri
	if lllink == "file":
	        return False
	
	if lllink=="about":
		'''about dialog, need to add LDC members whom helped'''
		about = gtk.AboutDialog()
        	about.set_program_name("Linux Lite Control Center")
        	about.set_version("0.1")
        	about.set_license('''This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA. ''')
        	about.set_authors(["Johnathan 'ShaggyTwoDope' Jenkins <shaggytwodope@linuxliteos.com>"])
        	about.set_comments(("Designed for Linux Lite"))
        	about.set_website("http://www.linuxliteos.com")
        	about.set_logo(gtk.gdk.pixbuf_new_from_file("/usr/share/litecc/litecc.png"))
        	about.run()
        	about.destroy()
        	return True

	if lllink == "admin":
	        
		#TODO: Better exec of admin functions.
		#if lllink.startswith("admin_admin_"):
			#execute("gksu " + lllink.split('admin_admin_')[1], ret=False)
		#else:
		execute(path)
		return True
		

		return True
	if lllink == "exportdetails":
		dialog = gtk.FileChooserDialog(("Select folder to export details to."), None,
   	gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
		    export_details(dialog.get_filename())
		dialog.destroy()
		return True
	#uses executep to pipe process fork
	if lllink == "script":
		executep("/usr/share/litecc/scripts/" + path) 
		return True
			
	# need to fix urls		
	if lllink == "help":
		execute("xdg-open file:///usr/share/doc/xfce4-utils/html/C/index.html")
		return True
		
	if lllink == "forum":
		execute("xdg-open http://www.linuxdistrocommunity.com/forums/forumdisplay.php?fid=62")
		return True

	if lllink == "website":
		execute("xdg-open http://www.linuxliteos.com/")
		return True
		
	if lllink == "irc":
		execute("xdg-open http://webchat.freenode.net/?channels=linuxlite")
		return True

	if lllink == "facebook":
		execute("xdg-open https://www.facebook.com/pages/Linuxlite/572323192787066")
		return True
		
	if lllink == "twitter":
		execute("xdg-open http://www.twitter.com/linuxlite/")
		return True

	if lllink == "google":
		execute("xdg-open https://plus.google.com/+linuxliteos/")
		return True

		

def get_info(info):
	'''here we gather some over all basic info'''
	try:
		if info=="os": return open('/etc/llver', 'r').read().split('\\n')[0]
		if info=="arc": return os.uname()[4]
		if info=="host": return os.uname()[1]	
		if info=="kernel": return os.uname()[0] +' '+ os.uname()[2]
		if info=="processor": return execute("cat /proc/cpuinfo | grep 'model name'").split(':')[1]
		if info=="mem": 
			mem = execute("free -m|awk '/^Mem:/{print $2}'")
			if  float(mem) > 1024:
				return str(round(float(mem) / 1024)) + " GB"
			else:
				return mem + " MB"
		if info=="gfx": return execute("lspci |grep VGA").split('controller:')[1].split('(rev')[0].split(',')[0]
		if info=="audio": return execute("lspci |grep Audio").split('device:')[1].split('(rev')[0].split(',')[0]
		#if info=="eth": return execute("lspci |grep Ethernet").split('controller:')[1].split('(rev')[0].split(',')[0]
		#if info=="desk": return execute("echo $XDG_CURRENT_DESKTOP")
		if info=="netstatus": return execute("ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo Active || echo Not connected to any known network")
		if info=="netip": return execute("hostname -I")
	except:
		return " "
def export_details(file):
	x = open(file+"/details.txt", "w");
	x.write('''
Operating system : %s
Kernel : %s
=============================
Processor : %s
Archticture : %s
RAM : %s
=============================
Devices : 
%s
=============================
Hard disks :

=============================
Mount Points : 



this file generated by lite control center at '''
%(get_info("os"), get_info("kernel"), get_info("processor"), 
get_info("arc"), get_info("mem"), execute("lspci -mm") ) )

def get_modules(section):
	'''we try and load errrors'''
	try:
		mod_dir=os.listdir("/usr/share/litecc/modules/%s/" %(section))
	except Exception, details:
		os.system("zenity --error --text 'Error : %s' --title 'Module Loading Error'" %(details))
		exit()
   	
	if mod_dir==[]:
		return "<p>" + ("no modules found!") + "</p>"
	else:
		parser = SafeConfigParser()
		admin=""
		for i in mod_dir :
			parser.read("/usr/share/litecc/modules/%s/%s" %(section, i))
			'''look for icons'''
			ico =parser.get('module', 'ico')
			#check if the icon exists
			ico="/usr/share/litecc/frontend/icons/modules/" + ico
			
			#check if the name has a different language
			if parser.has_option('module', 'name[%s]'):
				name = parser.get('module', 'name[%s]')
			else: name = parser.get('module', 'name')
			
			#check if the description has a different language
			if parser.has_option('module', 'desc[%s]'):
				desc = parser.get('module', 'desc[%s]')
			else: desc = parser.get('module', 'desc')
			
			#if parser.has_option('module', 'root'):
				#if parser.get('module', 'root') == "true":
					#command = "admin_" + parser.get('module', 'command')
					#command = "gksu " + parser.get('module', 'command')
			#else:
			#admin or root weren't used from the version 0.3 
			
			command = parser.get('module', 'command')
			command = command.replace("'", ''' \\' ''')
			
			admin+='''<div class="launcher" onclick="location.href='admin://%s'" >
			<img src="%s" onerror='this.src = "/usr/share/litecc/frontend/icons/modules/notfound.png"'/>
			<h3>%s</h3>
			<span>%s</span>
			</div>''' % ( command, #command
			ico,   #icon 
			name,  #name 
			desc ) #description 
		return admin
		
def frontend_fill():
	'''build all html junk'''
	
	filee=open(app_dir + '/frontend/default.html', 'r')
	page=filee.read()
	page=page.replace("{DIR_dir}", "ltr")

	
	page=page.replace("{string_1}", ("System Information"))
	page=page.replace("{string_2}", ("A brief overview of your system."))
	page=page.replace("{string_3}", ("Computer"))
	page=page.replace("{string_4}", ("Operating system: "))
	page=page.replace("{string_5}", ("Processor: "))
	page=page.replace("{string_6}", ("Architecture: "))
	page=page.replace("{string_7}", ("Installed Memory: "))
	page=page.replace("{string_8}", ("Devices"))
	page=page.replace("{string_9}", ("Graphics Card: "))
	page=page.replace("{string_10}", ("Sound Card: "))
	page=page.replace("{string_11}", ("Ethernet: "))
	page=page.replace("{string_12}", ("Misc"))
	page=page.replace("{string_13}", ("Hostname: "))
	page=page.replace("{string_14}", ("Kernel: "))
	page=page.replace("{string_15}", ("UNUSED"))
	page=page.replace("{string_16}", ("Software"))
	page=page.replace("{string_17}", ("Installing and maintaining software on your system."))
	page=page.replace("{string_18}", ("Desktop"))
	page=page.replace("{string_19}", ("Manage your desktop environment."))
	page=page.replace("{string_20}", ("System"))
	page=page.replace("{string_21}", ("This is a set of useful tools for your system."))
	page=page.replace("{string_22}", ("Hardware"))
	page=page.replace("{string_23}", ("Hardware management and configuration for your computer."))
	page=page.replace("{string_24}", ("Other Tools"))
	page=page.replace("{string_25}", ("all other tools that aren't related to any of these categories."))
	page=page.replace("{string_26}", ("Forum"))
	page=page.replace("{string_27}", ("Help"))
	page=page.replace("{string_28}", ("Install Popular Software"))
	page=page.replace("{string_29}", ("One click installs for some of your favourite applications. Be careful to select either the 32bit or 64bit installer for some software. Hover over each icon if you are not sure."))
	page=page.replace("{string_30}", ("Status: "))
	page=page.replace("{string_31}", ("Local IP Address: "))
	page=page.replace("{string_32}", ("Internet"))
	page=page.replace("{string_33}", ("UNUSED"))
	page=page.replace("{string_34}", ("UNUSED"))
	page=page.replace("{string_35}", ("Install Desktop Extras"))
	page=page.replace("{string_36}", ("Here you can install Desktop addons, select one to install."))
	page=page.replace("{string_37}", ("Export system details"))
	page=page.replace("{string_38}", ("UNUSED"))
	page=page.replace("{string_39}", ("UNUSED"))
	page=page.replace("{string_40}", ("save packages"))
	page=page.replace("{string_41}", ("Hardware drivers and players"))
	page=page.replace("{string_42}", ("Manage Hardware on your system."))
	page=page.replace("{string_43}", ("Nvidia graphics card driver"))
	page=page.replace("{string_44}", ("Bluetooth driver"))
	page=page.replace("{string_45}", ("Camera driver"))
	page=page.replace("{string_46}", ("Scanner driver"))
	page=page.replace("{string_47}", ("Website"))
	page=page.replace("{string_48}", ("IRC"))
	page=page.replace("{string_49}", ("Facebook"))
	page=page.replace("{string_50}", ("Twitter"))
	page=page.replace("{string_51}", ("Google+"))


	for i in ['os', 'arc', 'processor', 'mem', 'gfx', 'audio', 'kernel', 'host', 'netstatus', 'netip'] :
		page=page.replace("{%s}" %(i), get_info(i))

	for i in ['software', 'system', 'desktop', 'hardware', 'other'] :
		page=page.replace("{%s_list}" %(i), get_modules(i))
	filee.close()
	return page

def main(frontend):
	global browser
	global window
	window = gtk.Window()
	window.connect('destroy', gtk.main_quit)
	window.set_title(("Linux Lite Control Center"))
	window.set_icon(gtk.gdk.pixbuf_new_from_file("/usr/share/litecc/litecc.png"))
	window.set_size_request(830, 550)
	#Valtam do we need to resize window?
	window.set_resizable(True)
	window.set_position(gtk.WIN_POS_CENTER)
	browser = webkit.WebView()
	swindow = gtk.ScrolledWindow()
	window.add(swindow)
	swindow.add(browser)
	window.show_all()
	browser.connect("navigation-requested", functions)
	browser.load_html_string(frontend, 'file:///usr/share/litecc/frontend/')
	#no right click menu
	settings = browser.get_settings()
	settings.set_property('enable-default-context-menu', False)
	browser.set_settings(settings) 
try:
	import gtk
	import webkit
	import subprocess
	import os
	from ConfigParser import SafeConfigParser
	from locale import getdefaultlocale
	import urllib2
	import time
	from time import sleep

	app_dir='/usr/share/litecc'
	lang=getdefaultlocale()[0].split('_')[0]
	frontend = frontend_fill()
	main(frontend)
	#Ideally we dont need sleep if modules load fast enough
	#sleep(1)
	gtk.main()
	
except Exception, details:
	try:
		os.system("zenity --error --text 'Error : %s' --title 'Details Error'" %(detail))
	except:
		print details
	exit()
	
