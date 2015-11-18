from nose.tools import assert_true
from timing-rp import *

def Test_A():
	with tlogevents('bin/oggi.csv') as t:
		