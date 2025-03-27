from dispatch import dispatch
from users import users
from q import q
from gpu import gpu
from users import users
import threading
from data import data 
from inspector import inspector
#from policy import policy

#model A: a = 5/12, b = 10/3, SLO = 20 (100 times)
#config
ms_to_s = 0.001
alpha = 0.001
beta = 0.025 # s
SLO = 100 * ms_to_s # s
epsilon = 0.0 # s
throughput_ref = 500 # reqs/s
rate = 0.95 #90%
lmbd = rate * throughput_ref # lambd reqs/s
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
my_dspch = dispatch(SLO, my_q, my_gpu, epsilon, total_time, batch_size_data)
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
print(drop_reqs_data)
drop = drop_reqs_data.sum()
drop_rate = drop / my_users.total_reqts()

print(f'EBS = {EBS}')
print(f'ENq = {ENq}')
print(f'EResp = {EResp}')
print(f'drop rate = {drop_rate}')




	