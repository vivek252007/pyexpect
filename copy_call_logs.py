import paramiko,time
from librar import login_sa,logout_sa,login_admin

def scp_logs(server,passwrd,expect_line,log_command,log_ext):
	print "Executing scp"
	ssh,chan=scp_server(server,passwrd,expect_line,log_ext)
	logout_sa(ssh)
	sa_remove(server,passwrd,expect_line,log_ext)
	scp_local_machine(log_ext)

def scp_server(server,passwrd,expect_line,log_ext):
	print "login_sa for scp"
	ssh,chan = login_admin()
	chan.send("scp "+server+":/tmp/call_logs"+log_ext+" /tmp/\n")
	print "copying file"
	buff = ''
	while not buff.endswith(server+"'s password: "):
		resp = chan.recv(9999)
		#print resp
		buff += resp
	chan.send(passwrd+'\n')
	print "entering transcoder password"
	return ssh,chan

def sa_remove(server,passwrd,expect_line,log_ext) :
	ssh,chan=login_sa(server,passwrd,expect_line)
	chan.send('rm /tmp/call_logs'+log_ext+ '\n')
	time.sleep(2)
	chan.send('y \n')
	ssh.close()	
	logout_sa(ssh)

def scp_local_machine(log_ext):
	import scp, pexpect
	ssh,chan = login_admin()
	scp_file = scp.SCPClient(chan.get_transport())
	scp_file.get("/tmp/call_logs"+log_ext, local_path = '/home/vivek/Desktop')
	print "copying the file to the Desktop"
	time.sleep(2)
	chan.close()
	foo = pexpect.spawn('TO REMOTE IP'+log_ext)
	print "ssh to admin to remove file"
	foo.expect(" Expected line for eg. password: ")
	foo.sendline('YOUR PASSWORD')
	print "password entered"
	foo.expect(pexpect.EOF)
	print foo.before
