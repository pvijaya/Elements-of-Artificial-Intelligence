import sys
def gettuple(str,result):
	for tup in result:
		s = set(tup)
		if str in s:
			return tup
	return 0 
def checkconditions(result):
	checkset = {}
	if gettuple('Candelabrum',result) == 0:
		return 0
	
	p = gettuple('Candelabrum',result)[0]
	i = 'Banister'
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p]=i
	if gettuple('Banister',result) == 0 or gettuple('Irene',result) == 0:
		return 0
		
	p = gettuple('Banister',result)[0]
	i = gettuple('Irene',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p]= i
	p = 'Frank'
	i = 'Doorknob'
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i
	
	if  gettuple('Kirkwood',result) == 0 or gettuple('George',result) == 0:
		return 0
	p = gettuple('Kirkwood',result)[0]
	i = gettuple('George',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i	
	if  gettuple('Lake Avenue',result) == 0 or gettuple('Kirkwood',result) == 0:
		return 0 
	p = gettuple('Lake Avenue',result)[0]
	i = gettuple('Kirkwood',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i
	if  gettuple('Heather',result) == 0 or gettuple('Orange Drive',result) == 0:
		return 0 
	p = gettuple('Heather',result)[0]
	i= gettuple('Orange Drive',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i	
	if  gettuple('Heather',result) == 0 or gettuple('Jerry',result) == 0:
		return 0 
	p = gettuple('Jerry',result)[0] 
	i = gettuple('Heather',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i
	if  gettuple('North Avenue',result) == 0 or gettuple('Elephant',result) == 0:
		return 0 
	p = gettuple('North Avenue',result)[0] 
	i = gettuple('Elephant',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i
	if  gettuple('Maxwell Street',result) == 0 or gettuple('Elephant',result) == 0:
		return 0 
	p = gettuple('Elephant',result)[0]
	i = gettuple('Maxwell Street',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i	
	if  gettuple('Maxwell Street',result) == 0 or gettuple('Amplifier',result) == 0:
		return 0 
	p = gettuple('Maxwell Street',result)[0]
	i = gettuple('Amplifier',result)[2]
	if p in checkset and checkset[p] != i:
		return 0
	checkset[p] = i	
	
	return 1
	
	

cities = ["Maxwell Street", "Lake Avenue", "Kirkwood", "Orange Drive","North Avenue" ]
items = ["Candelabrum","Banister","Amplifier","Elephant","Doorknob"]
persons = ["Frank","George","Heather","Jerry","Irene"]
list_90 = []
for x in cities:
	for y in items:
		for z in persons:
			if(z=='Irene' and y == 'Banister'):
				continue
			if(z=='Frank' and y == 'Doorknob'):
				continue
			if(z=='George' and x =='Kirkwood'):
				continue
			if(z=='Heather' and x =='Orange Drive'):
				continue
			if(y=='Elephant' and x=='North Avenue'):
				continue
			if(y=='Elephant' and x=='Maxwell Street'):
				continue
			if(y=='Amplifier' and x=='Maxwell Street'):
				continue
			list_90.append([z,x,y])
print len(list_90)
set_all = set()
result = []
for i in list_90:
	set_all.add(i[0])
	set_all.add(i[1])
	set_all.add(i[2])
	for j in list_90:
		if(j[0] in set_all or j[1] in set_all or j[2] in set_all):
			continue
		else:
			set_all.add(j[0])
			set_all.add(j[1])
			set_all.add(j[2])
		for k in list_90:
			if(k[0] in set_all or k[1] in set_all or k[2] in set_all):
				continue
			else:
				set_all.add(k[0])
				set_all.add(k[1])
				set_all.add(k[2])	
			for l in list_90:
				if(l[0] in set_all or l[1] in set_all or l[2] in set_all):
					continue
				else:
					set_all.add(l[0])
					set_all.add(l[1])
					set_all.add(l[2])
				for m in list_90:
					if(m[0] in set_all or m[1] in set_all or m[2] in set_all):
						continue
					else:
						set_all.add(m[0])
						set_all.add(m[1])
						set_all.add(m[2])
						result = [i,j,k,l,m]
						r = checkconditions(result)
						if(r==1):
							print "result found"
							print result	
							sys.exit()
					set_all.remove(m[0])
					set_all.remove(m[1])
					set_all.remove(m[2])
				set_all.remove(l[0])
				set_all.remove(l[1])
				set_all.remove(l[2])	
			set_all.remove(k[0])
			set_all.remove(k[1])
			set_all.remove(k[2])	
		set_all.remove(j[0])
		set_all.remove(j[1])
		set_all.remove(j[2])
	result = {}
	set_all = set()

			
		
			
	
	
	

	


		