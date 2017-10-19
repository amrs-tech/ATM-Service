import getpass as gp
from datetime import datetime
import sys
from time import sleep
import os
import sendsms

def withdraw(uid,amount,num):
	wfile = open('balance.txt','r+')
	log = open('transac_log.txt','a')
	details = list(wfile)
	ans = ''
	for i in details:
		if uid in i:
			tempbal = int(i[4:])
			if amount < tempbal:
				tempbal -= amount
				details.remove(i)
				details.append(str(uid)+' '+str(tempbal)+'\n')
				for j in range(len(details)):
					ans += details[j]
				print '\nProcessing...' 
				sleep(2)
				wfile.seek(0)
				wfile.write(ans)
				print '\nCollect your Cash.' 
				sleep(1)
				t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				st = uid + '  ' + t + '  Rs.' + str(amount) + '  ATM WDL\n'
				log.write(st)
				msg = 'Your account is debited with Rs.'+str(amount)+'\n --Regards,\n IBS Bank.'
				sendsms.send('9751539433','scientist1',int(num),msg)
				break
			else:
				print('\n\tInsufficient Balance.\n')

def deposit(uid,amount,num):
	dfile = open('balance.txt','r+')
	log = open('transac_log.txt','a')
	details = list(dfile)
	ans = ''
	for i in details:
		if uid in i:
			tempbal = int(i[4:])
			print('\nInsert your cash.')
			sleep(2)
			tempbal += amount
			details.remove(i)
			details.append(str(uid)+' '+str(tempbal)+'\n')
			for j in range(len(details)):
				ans += details[j]
			print '\nProcessing...' 
			sleep(2)
			dfile.seek(0)
			dfile.write(ans)
			print '\nAmount Deposited.' 
			sleep(1)
			t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			st = uid + '  ' + t + '  Rs.' + str(amount) + '  CASH DEPOSIT\n'
			log.write(st)
			msg = 'Your account is credited with Rs.'+str(amount)+'\n --Regards,\n IBS Bank.'
			sendsms.send('9751539433','scientist1',int(num),msg)
			break
			
def checkbalance(uid):
	cbfile = open('balance.txt','r')
	details = list(cbfile)
	ans = ''
	for i in details:
		if uid in i:
			tempbal = i[4:]
			sleep(2)
			print('\nAccount Balance: '+tempbal)
			sleep(1)
			break

def changepin(uid,num):
	upfile = open('userpass.txt','r+')
	details = list(upfile)
	ans = ''
	for i in details:
		if uid in i:
			old = gp.getpass('Enter Old Pin: ')
			if old in i[4:]:
				new = gp.getpass('Enter New Pin: ')
				retype = gp.getpass('Re-type New Pin: ')
				if new == retype:
					details.remove(i)
					details.append(uid+' '+new+'\n')
					print('PIN Changed.')
					for j in range(len(details)):
						ans += details[j]
					upfile.seek(0)
					upfile.write(ans)
					msg = "Your IBS ATM pin has been changed. If you don't recognize this activity, Contact Bank."+'\n --Regards,\n IBS Bank.'
					sendsms.send('9751539433','scientist1',int(num),msg)
				else:
					print('Try Again !\n')
					changepin(uid)
			else:
				print('Old PIN Mismatch. Try Next time.')
			break

def ministmt(uid):
	mfile = open('transac_log.txt','r')
	details = []
	os.system('clear')
	print(' -- Your last three transactions --\n')
	for i in mfile:
		if uid in i:
			details.append(i)
	if len(details) < 3:
		for i in range(-(len(details)),0):
			print details[i][5:], 
	else:	
		for i in range(-3,0):
			print details[i][5:], 
	sleep(2)


os.system('clear')
print('\t\t------- IBS ATM -------\n')
opt = 'y'
while opt == 'y':
	
	uid = raw_input('Enter User ID: ')
	pas = gp.getpass('Enter PIN: ')

	print('\n')
	users = open('users.txt','r')
	userpass = open('userpass.txt','r')

	flag = uflag = 0

	for i in userpass:
		if uid in i:
			uflag = 0
			if pas in i:
				flag = 1
				break
			else:
				flag = 0
			
			break
		else:
			uflag = 1

	if uflag == 1:
		print('\nYour account cannot be used. Contact Bank for details.\n')
		sys.exit()

	if flag == 0:
		print('\nPassword Mismatch. Try Next time.\n')
		continue

	os.system('clear')
	print('\n')
	for i in users:
		if uid in i:
			print('\t\t Welcome '+i[4:-11])
			num = i[-11:-1]
			break
	sleep(2)

	ch = int(raw_input('1.Withdraw\t\t2.Cash Deposit (New Facility)\n3.Check Balance\t\t4.Change PIN\n5.Mini Statement\n\nEnter choice: '))
	if ch == 1:
		amount = int(raw_input('Enter amount: '))
		withdraw(uid,amount,num)
	elif ch == 2:
		amount = int(raw_input('Enter amount: '))
		deposit(uid,amount,num)
	elif ch == 3:
		checkbalance(uid)
	elif ch == 4:
		changepin(uid,num)
	elif ch == 5:
		ministmt(uid)
	sleep(1)
	os.system('clear')
	opt = raw_input('\nDo you want to perform another transaction? [y/n]: ')
	os.system('clear')


print('\nThank You !\n')
