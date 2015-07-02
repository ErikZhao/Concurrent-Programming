from threading import Thread, Semaphore
from time import sleep
from timeit import Timer
import random
import time

rng = random.Random()
rng.seed(1000)

(Thinking, Eating) = (0,1)

eatarr = [0 for i in range(20)]

def left(i): return i

def right(i): return (i+1) % 20

#solution #1
footman = Semaphore(20)
def get_forks1(i):
	footman.acquire()
	fork[right(i)].acquire()
	fork[left(i)].acquire()

def put_forks1(i):
	fork[right(i)].release()
	fork[left(i)].release()
	footman.release()

def philosophize1(i):
	state = Thinking
	while eatarr[i]<=9:
		if state is Thinking:
			get_forks1(i)
			state = Eating
		else:
			eatarr[i] = eatarr[i]+1
			put_forks1(i)
			sleep(rng.random())
			state = Thinking



if __name__ == '__main__':
	fork = [Semaphore(1) for _ in range(20)]
def totime1():
	phil1 = [Thread(target=philosophize1, args=[i]) for i in range(20)]
	for p in phil1: p.start()
	for p in phil1: p.join()

timer=Timer(totime1)
print("solution footman Time elapse: {:0.3f}s".format(timer.timeit(1)))


#solution #2

eatarr = [0 for i in range(20)]

def get_forks2(i):
	if(left(i)==0):
		fork[left(i)].acquire()
		fork[right(i)].acquire()
	else:
		fork[right(i)].acquire()
		fork[left(i)].acquire()

def put_forks2(i):
	fork[left(i)].release()
	fork[right(i)].release()


def philosophize2(i):
	state = Thinking
	while eatarr[i]<=9:
		if state is Thinking:
			get_forks2(i)
			state = Eating
		else:
			eatarr[i] = eatarr[i]+1
			put_forks2(i)
			sleep(rng.random())
			state = Thinking



if __name__ == '__main__':
	fork = [Semaphore(1) for _ in range(20)]
def totime2():
	phil2 = [Thread(target=philosophize2, args=[i]) for i in range(20)]
	for p in phil2: p.start()
	for p in phil2: p.join()

timer=Timer(totime2)
print("solution leftie Time elapse: {:0.3f}s".format(timer.timeit(1)))

#solution #3
state3 = ['thinking'] * 20
sem = [Semaphore(0) for i in range(20)]
mutex = Semaphore(1)
eatarr = [0 for i in range(20)]

def get_forks3(i):
	mutex.acquire()
	state3[i] = 'hungry'
	test(i)
	mutex.release()
	sem[i].acquire()


def put_forks3(i):
	mutex.acquire()
	state3[i] = 'thinking'
	test(right(i))
	test(left(i))
	mutex.release()

def test(i):
	if state3[i] == 'hungry'and state3(left(i)) != 'eating' and state3(right(i)) != 'eating':
		state3[i] = 'eating'
		sem[i].release()
		

def philosophize3(i):
	state3[i] = 'thinking'
	while eatarr[i]<=9:
		if state3 == 'thinking':
			get_forks3(i)
			state3[i] = 'eating'
		else:
			eatarr[i] = eatarr[i]+1
			put_forks3(i)
			sleep(rng.random())
			state3[i] = 'thinking'

if __name__ == '__main__':
	def totime3():
		phil3 = [Thread(target=philosophize3, args=[i]) for i in range(20)]
		for p in phil3: p.start()
		for p in phil3: p.join()

timer=Timer(totime3)
print("solution Tanenbaum's Time elapse: {:0.3f}s".format(timer.timeit(1)))





		
		





		
		
