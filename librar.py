import paramiko,time

def 	login_admin():
	print "login admin machine"
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('REMOTE IP', username='root', password='REMOTE IP PASSWORD')
	print "connection to remote ip"
	stdin, stdout, stderr = ssh.exec_command('hostname')
	print stdout.read()
	chan = ssh.invoke_shell()
	print "Invoking admin shell"
	chan.send('\n')
	return ssh,chan

def 	login_sa(server,passwrd,expect_line):
	print "login_server"
	ssh,chan = login_admin()
	chan.send("ssh "+server+"\n")
	print "connection established"
	#print chan.recv_stderr_ready()
	#print "ssh sawmill"
	buff = ''
	while not buff.endswith(server+"'s password: "):
		resp = chan.recv(9999)
		print resp
		buff += resp
	#time.sleep(2)
	# Send the password and wait for a prompt.
	chan.send(passwrd+'\n')
	print "transcoder Password entered"
	buff = ''
	while not buff.endswith(expect_line):
		resp = chan.recv(9999)
		print resp
		buff += resp
	# Execute reboot .
        return ssh,chan

def 	logout_sa(ssh):
	#print "logout_sa"
	ssh.close()
