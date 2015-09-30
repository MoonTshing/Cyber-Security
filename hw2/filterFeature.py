with open("../data/preprocessed.csv","r+") as original:
	with open("./feature.csv","w+") as feature:
		for line in original.readlines():
			tmp = line.split(",")
			feature.write(",".join(tmp[1:2])+","+",".join(tmp[3:9])+"\n")