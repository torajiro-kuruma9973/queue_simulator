from dispatch import dispatch
from users import users
from q import q
from gpu import gpu
from users import users
import threading
from data import data 
from inspector import inspector
#from policy import policy
import sys

#model A: a = 5/12, b = 10/3, SLO = 20 (100 times)
#config
sa = [0.001, 0.00105, 0.0011, 0.00115, 0.0012, 0.00125, 0.0013, 0.00135, 0.0014, 0.00145, 0.0015, 0.00155, 0.0016, 0.00165, 0.0017, 0.00175, 0.0018, 0.00185, 0.0019, 0.00195]
sb = [0.025, 0.02375, 0.0225, 0.02125, 0.02, 0.01875, 0.0175, 0.01625, 0.015, 0.01375, 0.0125, 0.01125, 0.01, 0.00875, 0.0075, 0.00625, 0.005, 0.00375, 0.0025, 0.00125]
print(len(sa) == len(sb))
n = len(sa)
i = 0
while i < n:
	ms_to_s = 0.001
	#alpha = float(sys.argv[1])
	#beta = float(sys.argv[2])
	#rate = float(sys.argv[3])
	#print(f"alpha:{alpha}, beta:{beta}, rate:{rate}")
	rate = 0.90
	print(f"******************* {i+1}, rate:{rate} *****************************")
	alpha = sa[i]
	beta = sb[i] # s
	i = i + 1
	SLO = 100 * ms_to_s # s
	epsilon = 0.0 # s
	throughput_ref = 500 # reqs/s
	#rate = 0.90 #90%
	lmbd = rate * throughput_ref # lambd reqs/s
	nice = (1/lmbd)/2  # this value is used by dispathcer which need to give up the CPU for a short while  for in case the Q is always locked (mutex).
	POLICY = "early_drop"
	insp_freq = 0.1 # s
	# total running time
	total_time = 30 # seconds

	# recording data for statistic
	batch_size_data = data()
	Nq_data = data()
	response_time_data = data()
	drop_reqs_data = data()

	my_gpu = gpu(alpha, beta, response_time_data)
	my_q = q(my_gpu, drop_reqs_data)
	#my_plc = policy(my_q, POLICY, drop_reqs_data)
	my_dspch = dispatch(nice, SLO, my_q, my_gpu, epsilon, total_time, batch_size_data)
	my_users = users(lmbd, my_q, total_time)
	my_insptr = inspector(insp_freq, my_q, total_time, Nq_data)

	t1 = threading.Thread(target=my_users.run, args=())
	t2 = threading.Thread(target=my_dspch.run, args=())
	t3 = threading.Thread(target=my_insptr.run, args=())

	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()

	print("STOPPED!")

	EBS = batch_size_data.average()
	ENq = Nq_data.average()
	EResp = response_time_data.average()
	#print(drop_reqs_data)
	drop = drop_reqs_data.sum()
	drop_rate = drop / my_users.total_reqts()

	#batch_size_data.get_results()

	print(f'EBS = {EBS}')
	print(f'ENq = {ENq}')
	print(f'EResp = {EResp}')
	print(f'drop rate = {drop_rate}')




	