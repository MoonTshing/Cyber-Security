import pandas as pd
import math



#  move the common columns to the front of two files
kddArrangIndex={0:42,1:42, 5:6,6:7,7:24,8:30,9:35}
unswArrangIndex={0:43,1:43,5:8,6:9,7:43,8:33,9:43}
def rearrange(orgin, after,shiftMap):
	with open(orgin,"r") as originfile:
		with open(after,"w+") as arrangedfile:
			for l in originfile.readlines():
				line = l.split()
				for i in shiftMap.keys():
					line.insert(i, line.pop(shiftMap[i]))
				arrangedfile.write(" ".join(line)+"\n")
	

def mov():
	rearrange("data/kddcup.data_10_percent_modified.txt","data/kddRearrange.csv",kddArrangIndex)
	rearrange("data/UNSW_NB15_training-setmodified.txt","data/nuswrearrange.csv",unswArrangIndex)


# merged=concatFeatures("Label attack_cat duration protocol_type service src_bytes dst_bytes count same_srv_rate dst_host_same_srv_rate flag land wrong_fragment urgent hot num_failed_logins logged_in num_compromised root_shell su_attempted num_root num_file_creations num_shells num_access_files num_outbound_cmds is_host_login is_guest_login srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count dst_host_diff_srv_rate dst_host_same_src_port_rate dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate dst_host_rerror_rate dst_host_srv_rerror_rate".split(),"label attack_cat dur proto service sbytes dbytes is_sm_ips_ports ct_srv_src ct_srv_dst state spkts dpkts rate sttl dttl sload dload sloss dloss sinpkt dinpkt sjit djit swin stcpb dtcpb dwin tcprtt synack ackdat smean dmean trans_depth response_body_len ct_state_ttl ct_dst_ltm ct_src_dport_ltm ct_dst_sport_ltm ct_dst_src_ltm is_ftp_login ct_ftp_cmd ct_flw_http_mthd ct_src_ltm".split())

dfKdd = pd.read_csv("data/kddRearrange.csv",delimiter=" ")
dfnusw = pd.read_csv("data/nuswrearrange.csv", delimiter=" ")
kddFeature="Label attack_cat duration protocol_type service src_bytes dst_bytes count same_srv_rate dst_host_same_srv_rate flag land wrong_fragment urgent hot num_failed_logins logged_in num_compromised root_shell su_attempted num_root num_file_creations num_shells num_access_files num_outbound_cmds is_host_login is_guest_login srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count dst_host_diff_srv_rate dst_host_same_src_port_rate dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate dst_host_rerror_rate dst_host_srv_rerror_rate".split()
nuswFeature="label attack_cat dur proto service sbytes dbytes is_sm_ips_ports ct_srv_src ct_srv_dst state spkts dpkts rate sttl dttl sload dload sloss dloss sinpkt dinpkt sjit djit swin stcpb dtcpb dwin tcprtt synack ackdat smean dmean trans_depth response_body_len ct_state_ttl ct_dst_ltm ct_src_dport_ltm ct_dst_sport_ltm ct_dst_src_ltm is_ftp_login ct_ftp_cmd ct_flw_http_mthd ct_src_ltm".split()
corrKdd={}
corrNusw={}
pairKdd={}
pairNusw={}

def matchMissingCol():
	for kddname in dfKdd.columns.values.tolist()[9:]:
		for nuswName in dfnusw.columns.values.tolist()[9:]:
			try:
				c=dfKdd[kddname].corr(dfnusw[nuswName])
				if math.isnan(c) is not True:
					if kddname in corrKdd:
						if abs(c) >= corrKdd[kddname]:
							corrKdd[kddname] = abs(c)
							pairKdd[kddname] = nuswName
					else:
						corrKdd[kddname] = abs(c)
						pairKdd[kddname] = nuswName
			except ValueError:
				pass
	
	for nuswName in dfnusw.columns.values.tolist()[9:]:
		for kddname in dfKdd.columns.values.tolist()[9:]:
			try:
				c=dfnusw[nuswName].corr(dfKdd[kddname])
				if math.isnan(c) is not True:
					if nuswName in corrNusw:
						if abs(c) >= corrNusw[nuswName]:
							corrNusw[nuswName] = abs(c)
							pairNusw[nuswName] = kddname
					else:
						corrNusw[nuswName] = abs(c)
						pairNusw[nuswName] = kddname
			except ValueError:
				pass

# Extend two files fields to the same number
def extend():
	for key in nuswFeature[9:]:
		if key in pairNusw.keys():
			i = i+1
			print key, len(dfKdd.columns)
			dfKdd.insert(len(dfKdd.columns),key, dfKdd[pairNusw[key]],allow_duplicates=True)
		else:
			i=i+1
			dfKdd.insert(len(dfKdd.columns),key, '-')
	
	
	for i in xrange(9,len(kddFeature)):
		if kddFeature[i] in pairKdd.keys():
			dfnusw.insert(i,kddFeature[i],dfnusw[pairKdd[kddFeature[i]]])
		else:
			dfnusw.insert(i,kddFeature[i], '-')
	

dfKdd.append(dfnusw, ignore_index=True)

dfKdd.to_csv("data/preprocessed.csv")








