import csv
from pkg_resources import resource_filename as rscfn

def read_dx(fn):
	fn = rscfn(__name__, fn)
	with open(fn, mode='r') as f:
		d = {}
		for row in csv.reader(f, delimiter='|'):
			d[row[0].replace('.', '')] = row[1].replace('.', '')
		return d

def read_pr(fn):
	fn = rscfn(__name__, fn)
	with open(fn, mode='r') as f:
		d = {}
		next(f)
		for row in csv.reader(f, delimiter=','):
			d[row[0].replace('.', '')] = row[1].replace('.', '')
		return d

def read_new_zealand(fn):
	fn = rscfn(__name__, fn)
	with open(fn, mode='r') as f:
		d = {}
		next(f)
		for row in csv.reader(f, delimiter=','):
			d[row[2]] = row[1]
		return d