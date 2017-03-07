import pprint
import copy
import random
from bottle import route,run,Bottle,template,request

file_name ="poker_data.txt"
f=open(file_name,'r')
g=open("input.txt",'r')
app=Bottle()

#li={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{}}
#prob_list={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{}}
li=[{},{},{},{},{},{},{},{},{},{}]
prob_list=[{},{},{},{},{},{},{},{},{},{}]
test=[{},{},{},{},{},{},{},{},{},{}]
for line in f:
	line=line.strip()
	if len(line)>0:
		features=line.split(',')
		for i in range(0,10):
			number=features[i].lower()
			poker=features[-1].lower()
			if number not in li[i]:
				li[i][number]={}
			if poker in li[i][number]:
				li[i][number][poker]+=1
			else:
				li[i][number][poker]=1
test=copy.copy(li)
#pprint.pprint(li[0])
def poker_prob():
	temp=0
	"""for i in range(0,10):
		print "i="+str(i)
		for j in range(1,len(li[i])+1):
			print "j="+str(j)
			dis_dict=li[i][str(j)]
			lst1=dis_dict.keys()
			lst2=dis_dict.values()
			s=sum(lst2)
			ran=len(dis_dict)
			for k in range(0,ran):
				print "k="+str(k)
				prob_list[i][str(j)]={}
				prob_list[i][str(j)][lst1[i]]=round(float(lst2[k])/float(s),5)"""
	for k in li:
		#pprint.pprint(k)
		for p in k:
			#pprint.pprint(p[k])
			for m in k[p]:
				#pprint.pprint(k[p][m])
				#pprint.pprint(m)
				temp+=k[p][m]
			for m in k[p]:
				k[p][m]=round(float(k[p][m])/float(temp),15)

poker_prob()
prob_list=copy.copy(li)
li=copy.copy(test)
#pprint.pprint(li)

def max_probability(t,value,result):
	for k in li:
		#pprint.pprint(k)
		for p in k:
			if p==t:
				#pprint.pprint(k[p])
				for m in k[p]:
					if str(value)==str(m):
						#pprint.pprint(k[p][m])
						if result==0:
							result=k[p][m]
						else:
							result=round(result*k[p][m],15)
						#print result
	return result

@app.route('/')
def home():
	return template('poker')

#test=['1','3','2','6','4','1','3','10','4','4']
result_list={}
#pprint.pprint(prob_list)
"""result=0.0
for i in range(0,10):
	for j in range(0,10):
		result=max_probability(test[j],i,result)
	result_list[i]=result
pprint.pprint(result_list)
print "The maximum probability of poker class value is: "+str(max(result_list))"""
test=['','','','','','','','','','']

def max_value(mydict):
	temp=max(mydict.values())
	li=mydict.keys()
	for i in range(0,10):
		if temp==mydict[i]:
			return li[i]
@app.post('/user_inp')
def user_inp():
	return template('user_inp')

@app.post('/greet')
def greet():
		test[0]=request.forms.get('suit1')
		test[1]=request.forms.get('rank1')
		test[2]=request.forms.get('suit2')
		test[3]=request.forms.get('rank2')
		test[4]=request.forms.get('suit3')
		test[5]=request.forms.get('rank3')
		test[6]=request.forms.get('suit4')
		test[7]=request.forms.get('rank4')
		test[8]=request.forms.get('suit5')
		test[9]=request.forms.get('rank5')
		result=0.0
		for i in range(0,10):
			for j in range(0,10):
				result=max_probability(test[j],i,result)
			result_list[i]=result
		pprint.pprint(result_list)
		#print "The maximum probability of poker class value is: "+str(max(result_list))
		return template('greet',var=max_value(result_list))

@app.post('/random')
def random():
	count=0.0
	total=0.0
	for line in g:
		line=line.strip()
		if len(line)>0:
			features=line.split(',')
		result=0.0
		for i in range(0,10):
			test[i]=features[i]
		for i in range(0,10):
			for j in range(0,10):
				result=max_probability(test[j],i,result)
			result_list[i]=result
		var=max_value(result_list)
		if str(var)==str(features[10]):
			count+=1
		else:
			total+=1
	return template('random',result=round(float(count/total),5))

@app.post('/rand_inp')
def rand_inp():
	import random
	test[0]=str(random.randrange(1,5))
	test[1]=str(random.randrange(1,14))
	test[2]=str(random.randrange(1,5))
	test[3]=str(random.randrange(1,14))
	test[4]=str(random.randrange(1,5))
	test[5]=str(random.randrange(1,14))
	test[6]=str(random.randrange(1,5))
	test[7]=str(random.randrange(1,14))
	test[8]=str(random.randrange(1,5))
	test[9]=str(random.randrange(1,14))
	result=0.0
	for i in range(0,10):
		for j in range(0,10):
			result=max_probability(test[j],i,result)
		result_list[i]=result
	pprint.pprint(result_list)
	#print "The maximum probability of poker class value is: "+str(max(result_list))
	return template('rand_inp',var=max_value(result_list))

run(app,host='localhost',port=7777,debug=True)
