import time
from numpy import random

class gpu:

	def __init__(self, a, b, data):
		self.a = a
		self.b = b
		self.state = "IDLE"
		self.data = data # for recroding the response time of a job
		self.n = 0 # how many tasks have been processed
		
	def service_time(self, batch_size):
		
			return self.a * batch_size + self.b

	def process(self, job_list):
		self.state = "BUSY"
		#print(list)
		size = len(job_list)
		latency = self.service_time(size) #unit: second
		time.sleep(latency)
		current_time = time.time()
		#print(f'P time: {current_time}')
		#print(job_list)
		for job in job_list:
			self.data.save_data(current_time - job.time_stamp)

		self.n = self.n + size

		self.state = "IDLE"

	def batch_size_based_on_time(self, gpu_time):
		return int((gpu_time - self.b) / self.a)

	def get_state(self):
		return self.state

	def cal_throughput(self, t):
		return self.n / t

	def cal_max_batch_size(self, slo):
		#print(f"SLO: {slo}, alfa: {self.a}, beta: {self.b}")
		return int((slo / 2 - self.b) / self.a) 

	def get_N_processed(self):
		return self.n
