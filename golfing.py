from threading import Thread, Semaphore
from time import sleep
from timeit import Timer
import random

stash = 20
N = 5
golfer = 3
balls_on_field = 0

mutex = Semaphore(1)
mutex1 = Semaphore(1)
emptystash = Semaphore(0)
fullstash  = Semaphore(0)


# golfer
def golfers(id):
	while True:
		mutex.acquire()
		global stash
		global balls_on_field
		print("Golfer", id, "calling for bucket")
		if stash < 5:
			emptystash.release()
			fullstash.acquire()
			print("Golfer", id, "got", N, "balls")
		else:
			print("Golfer", id, "got", N, "balls")
		stash -= N
		mutex.release()
    		for i in range(0,N):
				mutex1.acquire()
				balls_on_field += 1
				# simulate "swinging" here with random sleep
				print("Golfer", id, " hit ball", i)
				mutex1.release()
				rng = random.Random()
				rng.seed(100)
				sleep(rng.random())

# cart
def cart():
	while True:
		emptystash.acquire()
		global stash
		global balls_on_field
		print("########################################################")
		print("Stash=", stash, "Cart entering field")
		stash += balls_on_field
		print("Cart done, gathered", balls_on_field, "balls; Stash =", stash)
		print("########################################################")
		balls_on_field = 0
		fullstash.release()


tc = Thread(target=cart)
tc.start()
for i in range(golfer):
	tg = Thread(target=golfers, args=[i])
	tg.start()

