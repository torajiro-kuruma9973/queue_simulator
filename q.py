import threading
import job
import time

class q:

	def __init__(self, gpu, data):
		self.Q = []
		self.mutex = threading.Lock()
		self.gpu = gpu
		self.data = data

	def q_input(self, job):
		self.mutex.acquire()
		self.Q.append(job)
		self.mutex.release()

	def q_output(self, idx, size):
		self.mutex.acquire()
		end = idx + size
		out = self.Q[idx:end]
		self.Q = self.Q[end:]
		self.mutex.release()
		print(f"out len: {len(out)}")
		return out

	def get_Nq(self):
		self.mutex.acquire()
		n = len(self.Q)
		self.mutex.release()
		return n

	def get_timestamp(self):
		#self.mutex.acquire()
		if len(self.Q) > 0:
			rst = self.Q[0].time_stamp
		else:
			rst = 0
		#self.mutex.release()
		return rst
		
	def __early_drop__(self, window, slo):
		self.mutex.acquire()
		max_size = 0
		max_idx = 0
		expacted_size = 0
		wait = False
		n = len(self.Q)
		crt_time = time.time()
		#print(f"now: {crt_time}")
		for idx, job in enumerate(self.Q):
			elapse = crt_time - job.time_stamp
			left_time = slo - elapse
			size = self.gpu.batch_size_based_on_time(left_time)
			left_jobs = n - idx
			actual_size = min(size, window, left_jobs)
			#print(f"job{job.id}, {job.time_stamp}, {left_time}, {size}, {window}, {n}")
			if actual_size > max_size:
				max_size = actual_size 
				max_idx = idx
				expacted_size = size
		#update Q: drop reqs before max_idx
		self.Q = self.Q[max_idx:]
		self.data.save_data(max_idx)
		if expacted_size > max_size: # still have time for waiting
			wait = True
		self.mutex.release()
		print(f"s:{max_size}, id:{max_idx}")
		return max_size, wait


