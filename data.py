class data:
	def __init__(self):
		self.result = []

	def save_data(self, val): # save a data
		#print(f'id = {self.id}: {self.result}')
		self.result.append(val)

	def average(self):
		self.result.pop() # the last data may be not effective
		return sum(self.result) / len(self.result)

	def sum(self):
		return sum(self.result)

	def get_results(self):
		print(self.result)
			