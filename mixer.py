from threading import Thread, Semaphore
from time import sleep
from timeit import Timer
import random
from itertools import cycle

nInPool = 0
leaders = 0
followers = 0
bandleaderend = Semaphore(0)
bandleaderstart = Semaphore(1)
mutex = Semaphore(2)
mutex1 = Semaphore(1)
dance = Semaphore(1)
leaderQueue = Semaphore(0)
followerQueue = Semaphore(0)
rendezvous = Semaphore(0)

def band_leader():
	for music in cycle(['waltz', 'tango', 'foxtrot']):
		global nInPool
		bandleaderstart.acquire()
		print("band leader start to play", music)
		sleep(0.1)
		bandleaderend.acquire()
		if nInPool == 0:
			print("band leader end to play", music)
			bandleaderstart.release()		
		#start_music(music)		
	    #end_music(music)

def leader(id):
	while True:
		mutex.acquire()
		global leaders
		global followers
		global lid
		global nInPool
		print("Leader", id, "entering floor")
		nInPool = nInPool+1
		if followers > 0:
			followers = followers-1
			followerQueue.release()
		else:
			leaders = leaders+1
			mutex.release()
			leaderQueue.acquire()
		dance.acquire()
		print("Leader", id, "and Follower",fid, "dancing" )
		dance.release()
		mutex1.release()
		print("leader", id, "getting back in line")
		nInPool = nInPool-1	
		print("follower", fid, "getting back in line")
		nInPool = nInPool-1	
		sleep(1)	
		#dance()
		bandleaderend.release()
		rendezvous.acquire()
		mutex.release()
			#enter_floor()
			#dance()
			#line_up()


def follower(id):
	while True:
		mutex.acquire()
		mutex1.acquire()
		global nInPool
		print("follower", id, "entering floor")
		nInPool = nInPool+1	
		global fid
		global leaders
		global followers
		fid = id
		if leaders > 0:
			leaders = leaders-1
			leaderQueue.release()
		else:
			followers = followers+1
			mutex.release()
			followerQueue.acquire()
		dance.acquire()
		dance.release()
		#dance()
		rendezvous.release()
		#enter_floor()
		#dance()
		#line_up()

tb = Thread(target=band_leader)
tb.start()
	
for j in range(2):
	tl = Thread(target=leader, args=[j])
	tl.start()
for i in range(5):
	tf = Thread(target=follower, args=[i])
	tf.start()
	sleep(1)

