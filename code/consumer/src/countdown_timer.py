import time

class CountdownTimer:
	def __init__(self, seconds):
		self.target_time = seconds
		self.start_time = 0
	
	def start(self):
		self.start_time = time.time()
	
	def elapsed_time(self):
		return time.time() - self.start_time if self.start_time > 0 else 0
	
	def time_remaining(self):
		return self.target_time - self.elapsed_time()
	
	def has_elapsed(self):
		return self.elapsed_time() >= self.target_time
	
	def has_started(self):
		return self.start_time > 0