import traceback
import os

# Function decorator: Takes care that exceptions within sub-threads get also printed and exits main thread
def escalate_thread_exceptions(function):
	def func_wrapper(*args, **kwargs):
		try:
			return function(*args, **kwargs)
		except Exception:
			print(traceback.format_exc())
			os._exit(1)
	return func_wrapper