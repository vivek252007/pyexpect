import paramiko,time
import led_status
from librar import login_sa,logout_sa,login_admin

def sawmill_logs(server,passwrd,expect_line,log_command,log_ext,myx_id) :
	#print "sawmill_logs"	
	print "Starting logs"
	ssh,chan=login_sal(server,passwrd,expect_line)
	#chan.send(log_command+'\n')
	#print log_command
	print "Please off-hook the phone when instructed"
	call_completed = 'False'
	call_completed = led_status.led_stats(myx_id,chan,log_command)
	if call_completed == 'Pass':
		time.sleep(60)
		print 'Is call completed : ' + str(call_completed)
		chan.send('^C\n')
		print "LOGS STOPPED"
	else :
		pass		
	logout_sa(ssh)
	return call_completed
	print "logout ssh"
