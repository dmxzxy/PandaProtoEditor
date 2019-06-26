# -*- coding: utf-8 -*-
import os
import sys
from string import strip
from datetime import datetime


class Logger(object):
	def __new__(cls):
		if not hasattr(cls, '_instance'):
			cls._instance = object.__new__(cls)
		return cls._instance

	def __init__(self):
		self.terminal = sys.stdout

	def start(self, filePath, postfix):
		self.logfile = open(filePath + "logfile_" + str(postfix) + ".txt", "a")

	def write(self, content):
		strContent = content
		if content != "\n":
			strTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
			# strContent = "[" + strTime + "] " + str(content)
		self.logfile.write(strContent)
		self.terminal.write(strContent)

	def flush(self):
		self.logfile.flush()
		# self.terminal.flush()

def start(filePath, postfix):
	logger = Logger()
	logger.start(filePath, postfix)
	sys.stdout = logger
	print("# start write log")

def flush():
	logger = Logger()
	logger.flush()
	sys.stdout = sys.__stdout__