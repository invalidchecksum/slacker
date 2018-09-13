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
		self.files_added = {}
		self.sc = SlackClient(st)
		self.channel = chan
		self.lastSendStatus=''
		self.message=''
		self.interval = inter
		self.logfile = '/home/ubuntu/slacker.log'
		
		self.wm = pyinotify.WatchManager()
		self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=self.on_loop)
		self.wm.add_watch('/ftp/', pyinotify.IN_CREATE, rec=True)
		
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
			#t = threading.Thread( target=self.notifier.loop, kwargs={'daemonize':False,'callback':self.on_loop} ) 
			self.notifier.loop()
			#t.start()
		except pyinotify.NotifierError, err:
			print err
		except Exception as err:
			print err
		except ValueError,err:
			print "something went wrong: "+err
		except:
			print "Uncaught exception: ",sys.exc_info()[0]
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
	def sendMsg(self):
		slackMsg = "New crash dumps in: "
		if (len(self.files_added) < 1):
			return 1
		for p in self.files_added:
			slackMsg += p+", "
		self.lastSendStatus = sc.api_call("chat.postMessage",channel=self.channel,text=slackMsg.rstrip(','))
		self.logger( "sent message,status: "+str(json.dumps(self.lastSendStatus)) )
		self.files_added.clear()
		return 0
	def on_loop(self,evt):
		p = os.path.dirname(evt.pathname)
		print p
		#self.files_added.append(evt.pathname)
		self.files_added[p] = True

f=open('slacker.log','w')
f.write("Starting...\n")
f.close()
slack_token=''
try:
	slack_token=os.environ["SLACK_OAUTH_TOKEN"]
except:
	if not slack_token:
		with open('/home/ubuntu/.slack_token','r') as f:
			slack_token=f.read().replace('\n','')
	
print slack_token
sc = SlackClient(slack_token)

slack = SlackManager(slack_token,'globallabs_pub',30)
