import paramiko, time, re, pexpect

def     led_stats(id,chan,log_command):
	ssh1 = paramiko.SSHClient()
	ssh1.load_system_host_keys()
	ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh1.connect('REMOTE IP', username='root', password='REMOTE IP PASSWORD')
	stdin, stdout, stderr = ssh1.exec_command('WRITE COMMED TO BE EXECUTED')
	data = stdout.read()
	print data
	stdin.flush
	stdout.flush
	stderr.flush
	patt=' [0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'
	matches=re.search(patt,data)
	if matches:
		vpn_ip=matches.group(0)	
		print vpn_ip[1:]
		chan1 = ssh1.invoke_shell()
		
		# Ssh and wait for the password prompt.
		chan1.send('ssh '+vpn_ip[1:]+'\n')
	
		buff = ''
		while not buff.endswith('\'s password: '):
			resp = chan1.recv(9999)
			print resp	
			buff += resp
		# Send the password and wait for a prompt.
		chan1.send('!ooma123\n')
		buff = ''
		while not buff.endswith('# '):
			resp = chan1.recv(9999)
			print resp			
			buff += resp
		time.sleep(2)
		chan1.send('fs_cli \n')
		print log_command
		all_line_hanged = '0'
		phone_off_hook = '0'
		call_going = 'Fail'
		for wait in range(0,60):
			chan1.send('ooma_led status \n')
			resp = chan1.recv(9999)
			a_line1 = resp.find("Line1:off")
	    		print "Line 1 = " + str(a_line1)
			a_line2 = resp.find("Line2:off")
			print "Line 2 = " + str(a_line2)
			if str(a_line1)=='-1' or str(a_line2)=='-1':
				print "Please Hang-up on all the lines of the telo."
				all_line_hanged = '0'
			else :
				print "All lines clear"
				all_line_hanged = '1'
				break
			time.sleep(1)
			wait=wait+1
		if all_line_hanged == '1':
			for wait in range(0,60):
				chan1.send('ooma_led status \n')
				resp = chan1.recv(9999)
				b_line1 = resp.find("Line1:on")
		    		print "Line 1 = " + str(b_line1)
				b_line2 = resp.find("Line2:on")
				print "Line 2 = " + str(b_line2)
				if str(b_line1) != '-1' or str(b_line2) != '-1':
					print "Strating the call"
					phone_off_hook = '1'
					break
				else :
					print "PLEASE OFF HOOK THE PHONE AND START THE CALL"
					phone_off_hook = '0'
				time.sleep(1)
				wait=wait+1
		else :
			print 'Your time to call all lines on the telo has elasped. Please start a new call.'
		if phone_off_hook == '1':
			chan.send(log_command+'\n')
			print "LOGS STARTED."
			for wait in range(0,60):
				chan1.send('ooma_led status \n')
				resp = chan1.recv(9999)
				c_line1 = resp.find("Line1:off")
		    		print "Line 1 = " + str(c_line1)
				c_line2 = resp.find("Line2:off")
				print "Line 2 = " + str(c_line2)
				if str(c_line1) !='-1' and str(c_line2) !='-1':
					print "Call terminated"
					call_going =  'Pass'
					break
				else :
					print "Call Ongoing"
					call_going = 'Fail'
				time.sleep(2)
				wait=wait+1
		else :
			print "Your off-hook time has elasped. Please start a new call."
		chan1.send("/exit")
		#chan1.send('^d')
		chan1.send('exit \n')
		return call_going
		
	else :
		print "Not getting vpn-ip"
		
#pref_transx("09D")
