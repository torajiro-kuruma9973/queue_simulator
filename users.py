import time
import job
from numpy import random

class users:

	def __init__(self, lmbd, q, total_time):
		self.lmbd = lmbd
		self.q = q
		self.total_time = total_time
		self.n = 0

	def run(self):
		start_time = time.time()
		while (time.time() - start_time) < self.total_time:
			x = random.exponential(scale = 1/self.lmbd, size = (1, 1))
			t = x[0][0]
			time.sleep(t)
			self.n = self.n + 1
			j = job.job(self.n)

			self.q.q_input(j)
			print(f'{self.n}:t:{j.time_stamp}')

	def total_reqts(self):
		return self.n
			
	def run_test(self):
		while 1 > 0:
			print(f'user')
			

		