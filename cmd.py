from resources import Computer, File
import Constants
import time

# Public variables
command_list = {};
home_computer = Computer("home", False, None)
current_computer = home_computer
computer_list = {}

# This function displays the the files to the user
def ls():
	if current_computer.files:
		print Constants.file_header
		for file in current_computer.files:
			if current_computer.files[file].encrypted:
				print file, "(encrypted)"
			else:
				print file
	else:
		print "No files."
	
# This functions displays the text of a file if not encrypted
def cat(file_name = None):
	if file_name:
		if file_name in current_computer.files:
			file = current_computer.files[file_name]
			if file.encrypted != True:
				print file.text
			else:
				print "File is encrypted, cannot display content."
		else:
			print "%s does not exist." % file_name
	else:
		print "Please enter name of file you wish to open."

def connect(name = None):
	if name != "":
		if name in computer_list:
			if computer_list[name].protected == False:
				global current_computer
				current_computer = computer_list[name]
				print "Connecting to %s..." % current_computer.name
				time.sleep(2)
				print "Connected to %s." % current_computer.name
			else:
				print name, "is password protected, cannot connect."
		else:
			print name, "does not exist or is not connected."
	else:
		print "No address given, try again.."
	
def disconnect():
	global current_computer
	current_computer = home_computer
	print "Disconnecting..."
	time.sleep(2)
	print "Disconnected."

#TODO: display computer's specs
def scan(computer_name = None):
	if computer_name:
		if computer_name in computer_list:
			print "Displaying %s's specs" % computer_name
		else:
			print computer_name, "does not exist or is not connected."
	else:
		print "Enter name of computer you wish to scan."

#TODO: Integrate cracking method
def crack(computer_name = None, password = None):
	if computer_name:
		if computer_name in computer_list:
			if computer_list[computer_name].protected == True:
				if password:
					if computer_list[computer_name].password == password:
						computer_list[computer_name].protected = False
						print "Access granted, you can now connect."
				else:
					#TODO: write cracking method
					print "Initializing cracking protocol..."
			else:
				print computer_name, "does not need to be cracked."
		else:
			print computer_name, "does not exist or is not connected."
	else:
		print "Please enter name of computer you wish to crack."

#TODO: implement method
def decrypt(file_name = None):
	if file_name:
		if file_name in current_computer.files:
			if current_computer.files[file_name].encrypted == True:
				#TODO: implement decrypt program
				print "TODO: running decrypting file."
			else:
				print file_name, "is not encrypted."
		else:
			print file_name, "does not exist."
	else:
		print "Enter filename."
	
def download(file_name = None):
	if file_name:
		if file_name in current_computer.files:
			print "Downloading %s..." % file_name
			home_computer.files[file_name] = current_computer.files[file_name]
			del current_computer.files[file_name]
			time.sleep(1)
			print "Transfer complete."
		else:
			print file_name, "is not a valid filename."
	else:
		print "Enter name of file you wish to download."

def upload(file_name = None, computer_name = None):
	if file_name and computer_name:
		if file_name in home_computer.files:
			if computer_name in computer_list:
				print "Transfering %s to %s..." % (file_name, computer_name)
				computer_list[computer_name].files[file_name] = home_computer.files[file_name]
				del home_computer.files[file_name]
				time.sleep(1)
				print "Transfer complete."
			else:
				print computer_name, "does not exist or is not connected."
		else:
			print file_name, "is not a valid filename"
	else:
		print "Enter valid file and computer name."
	
def help():
	print Constants.help
	
# Load the command list into the command_list dictionary
def load_commands():
	command_list["ls"] = ls
	command_list["cat"] = cat
	command_list["connect"] = connect
	command_list["disconnect"] = disconnect
	command_list["scan"] = scan
	command_list["crack"] = crack
	command_list["decrypt"] = decrypt
	command_list["download"] = download
	command_list["upload"] = upload
	command_list["help"] = help
	
def load_computers():
	computer_list["home"] = home_computer
	computer_list["test"] = Computer("test", False, None)
	computer_list["test"].files["test"] = File("test", "this is text", False)
	computer_list["test"].files["test2"] = File("test2", "super secret stuff", True)
	computer_list["test2"] = Computer("test2", True, "password")

def load_stage():
	load_computers()
	load_commands()
	
def cmd():
	while True:
		command = raw_input(current_computer.prompt).split()
		if command:
			if command[0] in command_list:
				if len(command) == 1:
					command_list[command[0]]()
					return command
				elif len(command) == 2:
					command_list[command[0]](command[1])
					return command
				elif len(command) == 3:
					command_list[command[0]](command[1], command[2])
					return command
				else:
					print "Too many parameters, re-enter command."
					return None
			else:
				print command[0], "is not a valid command"
				return None
		else:
			return None
			
def play():
	load_stage()
	while (True):
		command = cmd()
		if command == None: return
	
play()