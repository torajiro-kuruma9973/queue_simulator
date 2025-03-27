import time

class dispatch:
	loss = 0
	state = "WAIT_GPU_IDLE"
	stamp = 0
	#result = []
	lost = 0

	def __init__(self, nice, slo, q, gpu, epsilon, total_time, data):
		self.SLO = slo # unit: s
		self.q = q
		self.gpu = gpu
		self.epsilon = epsilon
		self.total_time = total_time
		self.data = data
		self.extra_time = 1 #second, to make sure process all the requets after users stopped
		self.longest_waiting_time = slo / 2 # unit: s
		self.max_size = gpu.cal_max_batch_size(slo)
		#print(f"max_size = {self.max_size}")
		self.job_picked_idx = 0
		self.size_to_be_processed = 0
		self.nice = nice

	def __clear__(self):
		self.size_to_be_processed = 0
		self.stamp = 0

	def time_is_enough(self, elapse, nq, gpu):
		t = gpu.service_time(nq)
		#print(f'E:{elapse + t + self.epsilon}')
		if elapse + t + self.epsilon < (self.SLO / 2):
			return True
		else:
			#print(f'E:{elapse + t + self.epsilon}')
			return False

	def run_test(self):
		while 1 > 0:
			print(f'dispatch')
			

	def run(self):
		start_time = time.time()
		wait = False
		while (time.time() - start_time) < self.total_time + self.extra_time:
			match self.state:
				case "WAIT_GPU_IDLE":
					#print("WAIT_GPU_IDLE")
					if self.gpu.get_state() == "IDLE":
						if self.q.get_Nq() > 0: # Q is not empty
							self.state = "FIND_BEST_IDX"
				
				#case "CHECK_Q":
					#print("CHECK_Q")
					#self.stamp = self.q.get_timestamp()
					#print(f'tmsp:{self.stamp}')
					
					#elapse = time.time() - self.stamp
					#print(f'elapse={elapse}')
					#nq = self.q.get_Nq()
					#print(f'nq={nq}')
					#if (nq >= self.max_size): # or (elapse >= self.longest_waiting_time):
						#print(f"{nq}, {elapse}")
						#self.state = "EXECUTE_GPU"
					#elif elapse >= self.longest_waiting_time:
						#self.state = "FIND_BEST_IDX"
					#else:
						#self.state = "CHECK_Q" # keep waiting
				
				case "FIND_BEST_IDX":
					self.size_to_be_processed, wait = self.q.__early_drop__(self.max_size, self.SLO)
					if wait:
						time.sleep(self.nice)
						self.state = "FIND_BEST_IDX"
					else:
						self.state = "EXECUTE_GPU"

				case "EXECUTE_GPU":
					#print("EXECUTE_GPU")
					self.data.save_data(self.size_to_be_processed)
					#print(f'B:{self.size_to_be_processed}')
					job_list = self.q.q_output(0, self.size_to_be_processed)
					#for job in job_list:
						#print(f"job:{job.id}")
					self.gpu.process(job_list)
					self.__clear__()
					self.state = "WAIT_GPU_IDLE"

				#case "DISPATCH_ERROR":
					#print("DISPATCH_ERROR")





		


