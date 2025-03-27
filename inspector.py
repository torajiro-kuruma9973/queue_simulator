import time
import job
from numpy import random

class inspector:
	#result = []

	def __init__(self, interval, q, total_time, data): 
		self.interval = interval # time interval of sampling. unit in second
		self.total_time = total_time
		self.q = q
		self.data = data
		self.extra_time = 1 #make sure it will terminate before other threads to avoid sampling abnormal values

	def run(self): # sampling the values of Nq, to estimate the average of Nq
		start_time = time.time()
		while (time.time() - start_time) < self.total_time - self.extra_time:
			time.sleep(self.interval)
			self.data.save_data(self.q.get_Nq())
			#self.result.append(self.q.get_Nq())
			