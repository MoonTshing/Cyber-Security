import os
import sys
import csv
import re

"""
	Reconnaissance	probe
	Backdoor		r2l
	DoS				dos
	Exploits		probe
	Analysis		probe
	Fuzzers			probe
	Worms			r2l
	Shellcode		u2r
	Generic			generic
	Normal 			normal
"""
# Attack types of kdd data
"""
	back dos
	buffer_overflow u2r
	ftp_write r2l
	guess_passwd r2l
	imap r2l
	ipsweep probe
	land dos
	loadmodule u2r
	multihop r2l
	neptune dos
	nmap probe
	perl u2r
	phf r2l
	pod dos
	portsweep probe
	rootkit u2r
	satan probe
	smurf dos
	spy r2l
	teardrop dos
	warezclient r2l
	warezmaster r2l
"""


attackMap={}
with open("data/kdd_attack_types.txt","r") as orgin:
	for f in orgin.readlines():
		t = f.split()
		if len(t) == 2:
			attackMap[t[0]] = t[1].strip()

# process the unit of kdd data from percent to (num in 100)

with open("data/kddcup.data_10_percent","r+") as kdd:
	with open("data/kddcup.data_10_percent_modified.txt","w+") as kmod:
		for line in kdd.readlines():
			l = line[:-2].split(",")
			for i in xrange(0,len(l)):
				if re.match("^\d+?\.\d+?$", l[i]) is not None:
					if float(l[i]) < 1:
						l[i] = str(int(float(l[i])*100))
					elif float(l[i]) == 1:
						l[i] = str(int(float(l[i])))
				elif l[i] in attackMap.keys():
					l[i] = attackMap[l[i]]
				if i== len(l)-1:
					if l[-1] == "normal":
						l.append("0")
					else:
						l.append("1")
				tmp = " ".join(l)
			kmod.write(tmp+"\n")

print "finish process kdd data"

with open("data/UNSW_NB15_training-set.csv","r+") as unsw:
	with open("data/UNSW_NB15_training-setmodified.txt","w+") as unswmod:
		for line in unsw.readlines():
			l = line.split(",")
			for i in xrange(0,len(l)):
				if l[i] in attackMap.keys():
					l[i] = attackMap[l[i]]
				tmp = " ".join(l[1:])
			unswmod.write(tmp)

print "finish process UNSW_NB15_training-set data"











