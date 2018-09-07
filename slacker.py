from slackclient import SlackClient
import os
import pyinotify
import sys
import threading
import json
import datetime

class SlackManager:
	def nothing(self,):
		self.logger("Message Text placeholder")
	def __init__(self, st, chan,inter=30.0):
		self.filesSinceLastMsg = -1
		self.sc = SlackClient(st)
		self.channel = chan
		self.lastSendStatus=''
		self.message=''
		self.interval = inter
		self.logfile = '/home/ubuntu/slacker.log'
		
		self.wm = pyinotify.WatchManager()
		self.notifier = pyinotify.Notifier(self.wm)
		self.wm.add_watch('/ftp', pyinotify.IN_CREATE)
		
		self.startTimer()
		self.createNotifier()
		return
	def logger(self,data):
		try:
			f = open(self.logfile,"a")
			f.write( '{date:%Y-%m-%d %H:%M:%S}'.format( date=datetime.datetime.now() ) )
			f.write(": "+data+"\n")
			f.close
		except Exception as err:
			print err
	def createNotifier(self,):
		try:
			#self.notifier.loop(daemonize=True,callback=self.on_loop,pid_file='/home/ubuntu/pyinotify.pid',stdout='/home/ubuntu/pyinotify.log')
			t = threading.Thread( target=self.notifier.loop, kwargs={'daemonize':False,'callback':self.on_loop} ) 
			t.start()
		except pyinotify.NotifierError, err:
			print err
		except Exception as err:
			print err
		except ValueError,err:
			print "something went wrong: "+err
		except:
			print "Uncaught exception: ",sys.exc_info()[0]
	def add(self,amount=1):
		self.filesSinceLastMsg+=amount
		return
	def startTimer(self,):
		try:
			self.tracker = threading.Timer(self.interval,self.timerExpire)
			self.tracker.start()
		except pyinotify.NotifierError, err:
			print err
		print "Started timer"
		self.logger("started timer")
		return
	def timerExpire(self):#extend timerExpire to change what happens on expiration
		self.sendMsg()
		self.startTimer()
		return
	def resetTimer(self,):#manually called by user to restart the timer
		tracker.cancel()
		startTimer()
		return
	def sendMsg(self,):
		self.logger("Called sendMsg() with files: "+str(self.filesSinceLastMsg))
		temp = self.filesSinceLastMsg
		self.filesSinceLastMsg = 0
		if (temp == 1):
			#self.nothing()
			self.lastSendStatus = sc.api_call("chat.postMessage",channel=self.channel,text="A new crash dump was added to the 6900PhoneLogs.")
		elif (temp > 1):
			#self.nothing()
			self.lastSendStatus = sc.api_call("chat.postMessage",channel=self.channel,text=str(self.filesSinceLastMsg)+" new crash dumps were added to the 6900PhoneLogs.")
		else:
			self.logger("No Calls Made")
			return 1
		self.logger( "sent message,status: "+str(json.dumps(self.lastSendStatus)) )
		self.filesSinceLastMsg=0
		return 0
	def on_loop(self,notifier):
		self.add()
		self.logger("Added a file, filesSinceLastSend: " + str(self.filesSinceLastMsg))
		#print "Called the on_loop() function. Files: "+str(self.filesSinceLastMsg)

f=open('slacker.log','w')
f.write("Starting...\n")
f.close()
slack_token=''
try:
	lack_token=os.environ["SLACK_OAUTH_TOKEN"]
except:
	if not slack_token:
		with open('/home/ubuntu/.slack_token','r') as f:
			slack_token=f.read().replace('\n','')
	
print slack_token
sc = SlackClient(slack_token)

slack = SlackManager(slack_token,'globallabs_pub',30)
