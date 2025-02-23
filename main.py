#!/usr/bin/python3
import requests
import json
import re
import os
import matplotlib.pyplot as plt
import yaml
import sys


# url=sys.argv[1]
#url ='https://devportal-staging.unx.sas.com/rest-apis/riskModelingCore-v1'
#def swagger_data(url):
#    data = (requests.get(url))
#    f = open('swagger.json', 'w', encoding='utf-8')
#    f.write(data.text)
#swagger_data(url)

with open("src/API_guru_dummy_Open_API_Spec.json", 'r') as yaml_in, open("output/swagger.json", "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
    json.dump(yaml_object, json_out)

file = open('output/swagger.json', 'r', encoding='utf-8')
x = file.read()
jsondata = json.loads(x)

all_endpoints=[]      ###To get List of endpoints
for all in jsondata['paths'].keys():
    all_endpoints.append(all)


def write_data(name,list):
    variable=open(name,'w')
    for i in list:
        variable.write(i+'\n')

def remove_dup(list_name,new_list):
    for i in list_name:
        if i not in new_list:
            new_list.append(i)

write_data('output/all_endpoints',all_endpoints)



all_methods = []     ###To get List of Api Endpoints with methods

for i in jsondata['paths'].keys():
    for j in jsondata['paths'][i].keys():
        keys = i + ':' + j.capitalize()
        all_methods.append(keys)

write_data('output/all_methods',all_methods)


have_duplicate_endpoints=[]
for i in all_endpoints:
    p=re.sub("[\/][\{].*?[\}]","/",i)
    #slash1=p.replace('//','/')
    hashpart1 = re.sub('[\#].*', '', p)
    have_duplicate_endpoints.append(hashpart1)

endpoints=[]
remove_dup(have_duplicate_endpoints,endpoints)

have_duplicate_methods=[]
for i in all_methods:
    q=re.sub("[\/][\{].*?[\}]","/",i)
    #slash2=q.replace('//','/')
    hashpart2 = re.sub('[\#].*[\:]', ':', q)
    have_duplicate_methods.append(hashpart2)

methods=[]
remove_dup(have_duplicate_methods,methods)

write_data("output/method_without_ids",methods)

write_data("output/endpoints_without_ids",endpoints)

#__________________________________________________________________________________________________
                    #________________TEST RESULT

inputs = []  #####Take Test result files as an input and merge

#path=sys.argv[2]
path = r"tests"
#path=os.environ['Testend_Points_Folder']
def Path(path):

    for root, dirs, files in os.walk(path):
        for i in files:
            inputs.append(os.path.join(root,i))
Path(path)


test_solution = []
for i in inputs:
    with open(i) as any:
        for line in any:
            test_solution.append(line.strip())

test_result_methods = []                          ###List of UNIQUE Tested API endpoints with methods
remove_dup(test_solution,test_result_methods)
#print(len(test_result_methods),'trm')

write_data('output/TestResult.txt',test_result_methods)

filter0=[]

for i in test_result_methods:
    if i[0]==i[1]=='/':
        i=i[1:]
    elif i[-1]==':':
        i=i+'Get'
    filter0.append(i)
#print('filter0',len(filter0))
filter1=[]

for i in filter0:
    if i.startswith("/"):
        filter1.append(i)

#print('filter1',len(filter1))
#write_data('Filter1',filter1) ##__________________unused

removed_ids_methods=[]
for i in range(0,len(filter1)):
    i_d=re.sub("[\/$][\{].*?[\}]", "", filter1[i])
    rmv=re.sub('\w*\d{1,}\w*',"",i_d)
    removed_ids_methods.append(rmv)

removed_duplicates=[]
remove_dup(removed_ids_methods,removed_duplicates)

filter3=[]
for i in removed_duplicates:
    a=i.split(":")
    a[-1]=a[-1].capitalize()
    a=(':'.join(a[:]))
    filter3.append(a)
#print('filter3',len(filter3))

dup_filter=[]
remove_dup(filter3,dup_filter)
removed_param=[]
for i in dup_filter:
    quest = i.split(':')
    para = quest[0].split('?')
    removed_param.append(para[0] + ':' + quest[-1])

#write_data('removed_para,',removed_param)  ##-----unused

def Remove5UpperWords(jointword, seperators):
    for seprt in seperators:
        words = jointword.split(seprt)
        for indx, word in enumerate(words):
            otherSeprts = list(seperators)
            otherSeprts.remove(seprt)
            for otherSeprt in otherSeprts:
                if otherSeprt in word:
                    words[indx] = Remove5UpperWords(word, [otherSeprt])
                    break
            else:
                cnt = len([letter for letter in word if letter.isupper()])
                if cnt >= 5:
                    words[indx] = ''

        jointword = seprt.join(words)
    return jointword

if __name__ == "__main__":

    for indx, word in enumerate(removed_param):
        removed_param[indx] = Remove5UpperWords(word, ['/', ':'])




tested_methods_rmvdup=[]
remove_dup(removed_param,tested_methods_rmvdup)

#write_data('remove_dup',tested_methods_rmvdup) ##_______________unused

tested_methods=[]
methods_not_found=[]                      #List of methods that are not present in all_methods
for i in tested_methods_rmvdup:                    #Remove methods that are not present in all methods
    if i in methods:
        tested_methods.append(i)
    elif i not in methods:
        methods_not_found.append(i)


test_result_endpoints=[]                ###List of tested API endpoints without methods
for i in tested_methods_rmvdup:
    u=i.split(':')
    u=u[:-1]
    for j in u:
        test_result_endpoints.append(j)

tested_endpoints_rmvdup = []                          ###List of UNIQUE Tested API endpoints without methods
remove_dup(test_result_endpoints,tested_endpoints_rmvdup)

tested_endpoints=[]
endpoints_not_found=[]                  #List of endpoints that are not present in all_endpoints
for i in tested_endpoints_rmvdup:                #Remove endpoints that are not present in all endpoints
    if i in endpoints:
        tested_endpoints.append(i)
    if i not in endpoints:
        endpoints_not_found.append(i)




write_data("output/test_endpoints",tested_endpoints)
write_data("output/tested_methods",tested_methods)



#______________________________________________________________________________________________________
                    #__________MISSED ENDPOINTS & METHODS______________


missed_endpoints = []    #MISSED ENDPOINTS
for i in endpoints:
    if i not in tested_endpoints :
        missed_endpoints.append(i)

missed_methods = []        #MISSED METHODS
for i in methods:
    if i not in tested_methods:
        missed_methods.append(i)

write_data("output/Missed Endpoints",missed_endpoints)
write_data("output/Missed Methods",missed_methods)


#____________________________________________________________________________________________________________________
                                        #___________Length of Lists__________

length_endpoints=len(endpoints)
length_methods=len(methods)
length_missed_endpoints=len(missed_endpoints)
length_missed_methods=len(missed_methods)       ### Length of Common Elements from the lists
length_tested_endpoints=len(tested_endpoints)
length_tested_methods=len(tested_methods)         ###No. of elements in "tested_methods" list

method_coverage=(length_tested_methods/length_methods)*100          ###Test Coverage Formula
endpoint_coverage=(length_tested_endpoints/length_endpoints)*100

endpoint_coverage=round(endpoint_coverage,2)     ###Rounding off upto 2 decimals
method_coverage=round(method_coverage,2)

#_____________________________________________________________________________________________________________
                                            #_______OUTPUT_______

def Cal_EndpointTest_Coverage():
    print("ENDPOINTS BASED TEST COVERAGE")
    print("Total Number of API Endpoints : ", length_endpoints)
    print("Total ENDPOINTS Tested : ", length_tested_endpoints)
    print("MISSED API endpoints : ", len(missed_endpoints), end="\n" * 2)  ###No. of Missed API endpoints
    print("Endpoints based Test Coverage : ",endpoint_coverage, '%', end="\n" * 2)
    print("Untested Endpoints :-", *missed_endpoints, sep="\n")
    print("\n"*3)


def Cal_MethodTest_Coverage():
    print("METHOD BASED TEST COVERAGE")
    print("Total Number of Endpoints with METHODS : ", length_methods)
    print("Total METHODS Tested : ", length_tested_methods)
    print("MISSED Endpoints METHODS : ", len(missed_methods), end="\n" * 2)  ###No. of Missed API endpoints
    print("API endpoints METHOD based Test Coverage : ",method_coverage,'%',end="\n"*2)
    print("Untested METHODS :-", *missed_methods,sep="\n")
Cal_EndpointTest_Coverage()
Cal_MethodTest_Coverage()

#_______________________________________________________________________________________________________________
                                #______HTML REPORT__________

table_endpoints = f"<table border=1 cellspacing=0 cellpadding=3>"      #####TABLE STARTS
for i in missed_endpoints:
    for n in i.split():
        table_endpoints+=f"<td>{i}</td>"
    table_endpoints+="<tr>"
table_endpoints+="</table>"


table_methods = f"<table border=1 cellspacing=0 cellpadding=3>"
for i in missed_methods:
    for n in i.split():
        table_methods+=f"<td>{i}</td>"
    table_methods+="<tr>"
table_methods+="</table>"                  ######TABLE ENDS


plt.figure(figsize=(5,2.5))          #####PIE CHART FOR ENDPOINTS
labels=['Covered Endpoints','Missed Endpoints']
cls=['g','r']
explode=(0.1,0)
values=[length_tested_endpoints,length_missed_endpoints]
plt.pie(values, labels=labels, autopct="%.2f%%", colors=cls, explode=explode)
plt.savefig('reports/pie_chart_endpoints.png')


plt.figure(figsize=(5,2.5))          #####PIE CHART FOR METHODS
labels=['Covered Methods','Missed Methods']
cls=['g','r']
explode=(0.1,0)
values=[length_tested_methods,length_missed_methods]
plt.pie(values, labels=labels, autopct="%.2f%%", colors=cls, explode=explode)
plt.savefig('reports/pie_chart_methods.png')

new = open('reports/index.html', 'w')
work = f"""
<html>
	<head>
		<title>Test Coverage Report</title>

	</head>
	<body><code>
		<h1 style="text-align:center;"><u><b>COVERAGE REPORT</b></u></h1><br>
		<p><img style="border:3.5px solid black; float:right; width:450px; height:225px;" src = "pie_chart_endpoints.png" ;><br><br></p>
		<h3><u>Endpoints Based TEST COVERAGE</u> :-</h3>
		<p>Number of API Endpoints : {length_endpoints}</p>
		<p>Covered Endpoints : {length_tested_endpoints}</p>
		<p>Missed Endpoints : {length_missed_endpoints}</p>
		<p><b>TEST COVERAGE : {endpoint_coverage} %</p></b><br><br><br>
		<p><b> Missed Endpoints :</b><br><br>{table_endpoints}</p><hr><br><br>


		<p><img style="border:3.5px solid black; float:right; width:450px; height:225px;" src = "pie_chart_methods.png" ;><br><br></p>
		<h3><u>Method Based TEST COVERAGE</u> :-</h3>
		<p>Number of API Endpoints with Methods : {length_methods}</p>
		<p>Covered Methods : {length_tested_methods}</p>
		<p>Missed Methods : {length_missed_methods}</p>
		<p><b>TEST COVERAGE : {method_coverage} %</b></p><br>
		<p><b> Missed Methods </b>:<br><br> {table_methods}</p>

	</code></body>
</html>

"""
new.write(work)
new.close()

#####################     HTML REPORT ENDS    ######################
print('\n'*2)

if len(endpoints_not_found)==0:
	print("Endpoints not found in the list of all_endpoints : 0")
else:
	print("Endpoints not found in the list of all_endpoints : ")
	for i in endpoints_not_found:
		print(i)

print('\n\n')

if len(methods_not_found)==0:
	print("Methods not found in the list of all_methods : 0")
else:
	print("Methods not found in the list of all_methods :")
	for i in methods_not_found:
		print (i)



write_data("output/endpoints_not_found",endpoints_not_found)
write_data("output/methods_not_found", methods_not_found)
print('\n'*2)
print("Files inside Test Folder :")
for i in inputs:
	if len(inputs)==0:
		print("Folder is empty!")
	else:
		print (i)