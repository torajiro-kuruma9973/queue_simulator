class data:
	def __init__(self):
		self.result = []

	def save_data(self, val): # save a data
		#print(f'id = {self.id}: {self.result}')
		self.result.append(val)

	def average(self):
		return sum(self.result) / len(self.result)

	def sum(self):
		return sum(self.result)

	def get_results(self):
		print(self.result)
			