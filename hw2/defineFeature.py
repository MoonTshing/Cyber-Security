with open("./feature.csv","r+") as raw:
	with open("./featureInBinary.csv","w+") as fInBinary:
		for line in raw.readlines():
			tmp = line.rstrip().split(",")
			
		
			# duration
			if int(tmp[1]) > 1:
				tmp[1] = "0"
			else:
				tmp[1] = "1"

			# protocol_type
			if tmp[2] == 'tcp' or tmp[2] == 'udp':
				tmp[2] = "0"
			else:
				tmp[2] = "1"

			# service
			if tmp[3] == 'urh_i' or tmp[3] == 'telnet' or tmp[3] == 'domain_u' or tmp[3] == 'smtp' or tmp[3] == 'http':
				tmp[3] = "0"
			else:
				tmp[3] = "1"

			# src_bytes
			if (int(tmp[4]) >= 29 and int(tmp[4])<= 519) or (int(tmp[4])>=1481 and int(tmp[4]) <= 40494):
				tmp[4]="0"
			else:
				tmp[4]="1"

			# dst_bytes
			if int(tmp[5]) >= 5134218 and int(tmp[5]) <= 4:
				tmp[5] = "0"
			else:
				tmp[5] = "1"

			# count
			# print tmp[6]
			if int(tmp[6]) < 41:
				tmp[6] = "0"
			else:
				tmp[6] = "1"
			
			fInBinary.write(",".join(tmp)+"\n")

			