from django.shortcuts import render
from django.http import HttpResponse
import datetime
import csv
import re 
import urllib2
from conf import *
from collections import Counter,OrderedDict
from imap_app.forms import FilerForm
from django.http import HttpResponseRedirect 
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> Checked in pagerstats v1. Working drilldown 1
opsInvHostYes = "Below hosts found in Ops Inventory [Prod]"
opsInvHostNo = "No hosts found in Ops Inventory"
qbHostYes = "Below hosts found in Storage Quickbase but not in Ops Inv [Prod & Non Prod]"
qbHostNo = "No hosts found in Storage Quickbase" 

#def search_form(request):
#    return render(request, 'search_form.html')

def search(request):
    error = False

    
    if request.method == 'GET':

    
        form = FilerForm(request.GET)
        if form.is_valid():
            var = form.cleaned_data 
            if var['Type'] == 'filer':
<<<<<<< HEAD
                filername = var['filer']  #filer is the label name and not the filer name value 
=======
                filername = var['filer']  #filer is the label name and not the filer name value
                print filername
>>>>>>> Checked in pagerstats v1. Working drilldown 1
            elif var['Type'] == 'vfiler':  #Radio button selection 
                filername = getVfiler(var['filer']) 
    	        #Calling method to ge the data
            if filername != 'ERROR':
                env = 'PRD'
                out = open('OpsInv.csv', "w")  
                req = urllib2.Request('https://intuitcorp.quickbase.com/db/bhfic8446?a=API_GenResultsTable&apptoken=cp7q2atbp8rwbcb4jwytxcvw2ras&query={''12''.CT.'+env+'}&options=csv&username='+username+'&password='+pwd+'') 
                out.write(urllib2.urlopen(req).read()) 
                out.close() 
<<<<<<< HEAD

                out = open('/Users/shaveri/python_proj/apps/imap_project/imap_app/logs.csv', 'a') 
                out.write(filername+","+str(datetime.now()))
                out.write('\n')
                out.close
=======
>>>>>>> Checked in pagerstats v1. Working drilldown 1
                
                qdc_a_ops,qdc_a_qb = getQDC_A_hf(filername)
                qdc_b_ops,qdc_b_qb = getQDC_B_hf(filername)
                qdc_c_ops,qdc_c_qb = getQDC_C_hf(filername)
                qdc_e_ops,qdc_e_qb = getQDC_E_hf(filername)
                lvdc_a_ops,lvdc_a_qb = getLVDC_A_hf(filername)
                lvdc_b_ops,lvdc_b_qb = getLVDC_B_hf(filername) 
                getAppCountOps =  {}
                getAppCountQB = {}



                if qdc_a_ops or qdc_a_qb:
                	zone = "QDC A"
                	if qdc_a_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(qdc_a_ops) 
                		print getAppCountOps
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if qdc_a_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(qdc_a_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2
<<<<<<< HEAD
 
=======

                	print "I am herererererereree"	
>>>>>>> Checked in pagerstats v1. Working drilldown 1

                	return render(request, 'search_results.html', {'qdc_a_ops': qdc_a_ops,'qdc_a_qb': qdc_a_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                elif qdc_b_ops or qdc_b_qb:
                	zone = "QDC B"
                	if qdc_b_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(qdc_b_ops)
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if qdc_b_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(qdc_b_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2

                	return render(request, 'search_results.html', {'qdc_a_ops': qdc_b_ops,'qdc_a_qb': qdc_b_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                elif qdc_c_ops or qdc_c_qb:
                	zone = "QDC C"
                	if qdc_c_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(qdc_c_ops)
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if qdc_c_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(qdc_c_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2

                	return render(request, 'search_results.html', {'qdc_a_ops': qdc_c_ops,'qdc_a_qb': qdc_c_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                elif qdc_e_ops or qdc_e_qb:
                	zone = "QDC E"
                	if qdc_e_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(qdc_e_ops)
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if qdc_e_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(qdc_e_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2

                	return render(request, 'search_results.html', {'qdc_a_ops': qdc_e_ops,'qdc_a_qb': qdc_e_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                elif lvdc_a_ops or lvdc_a_qb:
                	zone = "LVDC A"
                	if lvdc_a_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(lvdc_a_ops)
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if lvdc_a_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(lvdc_a_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2

                	return render(request, 'search_results.html', {'qdc_a_ops': lvdc_a_ops,'qdc_a_qb': lvdc_a_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                elif lvdc_b_ops or lvdc_b_qb:
                	zone = "LVDC B"
                	if lvdc_b_ops:
                		qdc_ops = opsInvHostYes
                		getAppCountOps = appCount(lvdc_b_ops)
                	else:
                		qdc_ops = opsInvHostNo
                		error = 1
                	if lvdc_b_qb:
                		qdc_qb = qbHostYes
                		getAppCountQB = appCount(lvdc_b_qb)
                	else:
                		qdc_qb = qbHostNo
                		error = 2

                	return render(request, 'search_results.html', {'qdc_a_ops': lvdc_b_ops,'qdc_a_qb': lvdc_b_qb, 'zone':zone,'qdc_ops':qdc_ops,'qdc_qb' :qdc_qb,'getAppCountOps':getAppCountOps,'getAppCountQB':getAppCountQB,'form': form,'error':error})
                else:
                    form = FilerForm(request.GET)
<<<<<<< HEAD
                    message = 'No host found or Bad Input. Please try again or please follow the QuickBase.[https://intuitcorp.quickbase.com/db/bijddjssa?a=td]'
=======
                    message = 'Bad Input. Please try again or please follow the QuickBase.[https://intuitcorp.quickbase.com/db/bijddjssa?a=td]'
>>>>>>> Checked in pagerstats v1. Working drilldown 1
                return render(request, 'error_form.html', {'error': True,'form': form,'message':message})

            else: #if filername returns ERROR
                form = FilerForm(request.GET)
<<<<<<< HEAD
                message = 'No host found or Bad Input. Please try again or please follow the QuickBase.[https://intuitcorp.quickbase.com/db/bijddjssa?a=td]'
=======
                message = 'Bad Input. Please try again or please follow the QuickBase.[https://intuitcorp.quickbase.com/db/bijddjssa?a=td]'
>>>>>>> Checked in pagerstats v1. Working drilldown 1
            return render(request, 'error_form.html', {'error': True,'form': form,'message':message})
    else: 
        error = False
        form = FilerForm(request.GET)
    return render(request,'search_form.html', {'form': form,'error':error})

    

def appCount(apparray):
    l_appcount = []  
    service_Data = csv.reader(open('/Users/shaveri/python/scripts/service_lookup.csv','rU'))
    service = {}
    d_sorted_data = {}
    l_appSummary = {}

    for i in service_Data:
        service[i[1]] = i[7]  # getting App Name and App priority[7] from service lookup csv

    for i,j in apparray.items():
        l_appcount.append(apparray[i][2])

    d_sorted_data = OrderedDict(sorted(Counter(l_appcount).items()))

    for i,j in d_sorted_data.items():
    	if i in service:
    		l_appSummary[i] = [i]
    		l_appSummary[i].append(service[i][0])
    		l_appSummary[i].append(j)
    	else:
    		l_appSummary[i] = [i]
    		l_appSummary[i].append('NA')
    		l_appSummary[i].append(j)

<<<<<<< HEAD
    #return l_appSummary
    return OrderedDict(sorted(l_appSummary.items(), key=lambda e: e[1][0]))
=======
    return l_appSummary
>>>>>>> Checked in pagerstats v1. Working drilldown 1



def OpsInvData(): 
    f1 = open('OpsInv.csv', 'rU')
    csv_r1 = csv.reader(f1)
    recops={}   #OpsInv
    for i in csv_r1: 
        source = re.search("(.*?)\.(.*)", i[9])
        if source: 
            source_1 = source.group(1) 
            recops[source_1]=[i[6]]   #DC
            recops[source_1].append(i[7]) #ENV
            recops[source_1].append(i[8])  #App Name
        else: 
            recops[i[9]] = [i[6]]
            recops[i[9]].append(i[7])
            recops[i[9]].append(i[8]) 
    
    return recops


def getQDC_A_hf(filername):   
    rec_a_qb={}   #Dict with Host as key and filer as list
    rec_a_qb_det = {}
    rec_a = {} 
    rec_qdc_a_ops = {}
    rec_qdc_a_qb = {}
    recops = OpsInvData() 
    out = open('QDC_A.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bhj9677pa?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('QDC_A.csv','rU') 
    csv_r3 = csv.reader(qbData)
    
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_a:
                        rec_a[source_2].append(filer)  
                    else:
                        rec_a[source_2] = [filer] 
            else: 
                if i[2] in recops:
                    if i[2] in rec_a:
                        rec_a[i[2]].append(filer)
                    else:
                        rec_a[i[2]] = [filer]
                        
    for key,value in rec_a.items():
        if value  in rec_a.values():
            rec_a[key]=list(set(value))
   
    for k,v in rec_a.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_qdc_a_ops[k] = [filername] 
            rec_qdc_a_ops[k].append(k)
            rec_qdc_a_ops[k].append(recops[k][2])
            rec_qdc_a_ops[k].append(recops[k][1])#Env 
    
    qbData = open('QDC_A.csv','rU') 
    csv_r3 = csv.reader(qbData)
    for i in csv_r3:  
        if (i[9] == 'CTO'): 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)  
                if source_2 in rec_a_qb:
                    rec_a_qb[source_2].append(filer)
                else:
                    rec_a_qb[source_2] = [filer] 
                rec_a_qb_det[source_2]= [i[9]] # BUFG
                rec_a_qb_det[source_2].append(i[7]) #App
                rec_a_qb_det[source_2].append(i[4]) #Path
            else:
                if i[2] in rec_a_qb:
                    rec_a_qb[i[2]].append(filer)
                else:
                    rec_a_qb[i[2]] = [filer] 
                rec_a_qb_det[i[2]] = [i[9]]
                rec_a_qb_det[i[2]].append(i[7]) 
                rec_a_qb_det[i[2]].append(i[4])
                    
    for key,value in rec_a_qb.items():
        if value  in rec_a_qb.values():
            rec_a_qb[key]=list(set(value))
            
    for k,v in rec_a_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_a_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_qdc_a_qb[k] = [filername] 
            rec_qdc_a_qb[k].append(k)
            rec_qdc_a_qb[k].append(rec_a_qb_det[k][1]) #App Name 
    
<<<<<<< HEAD
    #return rec_qdc_a_ops,rec_qdc_a_qb
    return OrderedDict(sorted(rec_qdc_a_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_qdc_a_qb.items(), key=lambda e: e[1][2]))
=======
    return rec_qdc_a_ops,rec_qdc_a_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1




def getQDC_B_hf(filername):  
    recops = OpsInvData()   #OpsInv
    rec_b_qb={}   #Dict with Host as key and filer as list
    rec_b_qb_det = {}
    rec_b = {}
    rec_qdc_b_ops = {}
    rec_qdc_b_qb = {}
    print_var = None 
    out = open('QDC_B.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bhj968qhf?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('QDC_B.csv','rU') 
    csv_r3 = csv.reader(qbData)
    
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_b:
                        rec_b[source_2].append(filer)  
                    else:
                        rec_b[source_2] = [filer] 
            else: 
                if i[2] in recops:
                    if i[2] in rec_b:
                        rec_b[i[2]].append(filer)
                    else:
                        rec_b[i[2]] = [filer]
                        
    for key,value in rec_b.items():
        if value  in rec_b.values():
            rec_b[key]=list(set(value))

    for k,v in rec_b.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_qdc_b_ops[k] = [filername] 
            rec_qdc_b_ops[k].append(k)
            rec_qdc_b_ops[k].append(recops[k][2])
            rec_qdc_b_ops[k].append(recops[k][1])#Env 
    
    qbData = open('QDC_B.csv','rU') 
    csv_r3 = csv.reader(qbData)
    for i in csv_r3:  
        if (i[9] == 'CTO'):
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)  
                if source_2 in rec_b_qb:
                    rec_b_qb[source_2].append(filer)
                else:
                    rec_b_qb[source_2] = [filer] 
                rec_b_qb_det[source_2]= [i[9]] # BUFG
                rec_b_qb_det[source_2].append(i[10]) #App
                rec_b_qb_det[source_2].append(i[6]) #Path
            else:
                if i[2] in rec_b_qb:
                    rec_b_qb[i[2]].append(filer)
                else:
                    rec_b_qb[i[2]] = [filer] 
                rec_b_qb_det[i[2]] = [i[9]]
                rec_b_qb_det[i[2]].append(i[10]) 
                rec_b_qb_det[i[2]].append(i[6])
                    
    for key,value in rec_b_qb.items():
        if value  in rec_b_qb.values():
            rec_b_qb[key]=list(set(value))

    for k,v in rec_b_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_b_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_qdc_b_qb[k] = [filername] 
            rec_qdc_b_qb[k].append(k)
            rec_qdc_b_qb[k].append(rec_b_qb_det[k][1]) #BUFG 

    
<<<<<<< HEAD
    #return rec_qdc_b_ops,rec_qdc_b_qb
    return OrderedDict(sorted(rec_qdc_b_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_qdc_b_qb.items(), key=lambda e: e[1][2])) #Ordered Dictionary by app name
=======
    return rec_qdc_b_ops,rec_qdc_b_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1
            


def getQDC_C_hf(filername):  
    recops = OpsInvData()   #OpsInv
    rec_c_qb={}   #Dict with Host as key and filer as list
    rec_c_qb_det = {}
    rec_c = {} 
    rec_qdc_c_ops = {}
    rec_qdc_c_qb = {}
    out = open('QDC_C.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bhj96874m?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('QDC_C.csv','rU') 
    csv_r3 = csv.reader(qbData)
     
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[1])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_c:
                        rec_c[source_2].append(filer)  
                    else:
                        rec_c[source_2] = [filer] 
            else: 
                if i[1] in recops:
                    if i[1] in rec_c:
                        rec_c[i[1]].append(filer)
                    else:
                        rec_c[i[1]] = [filer]
                        
    for key,value in rec_c.items():
        if value  in rec_c.values():
            rec_c[key]=list(set(value))
    
    for k,v in rec_c.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_qdc_c_ops[k] = [filername] 
            rec_qdc_c_ops[k].append(k)
            rec_qdc_c_ops[k].append(recops[k][2])
            rec_qdc_c_ops[k].append(recops[k][1])#Env 
    
    qbData = open('QDC_C.csv','rU') 
    csv_r3 = csv.reader(qbData)
    for i in csv_r3:  
        if (i[9] == 'CTO'):
            source = re.search("(.*?)\.(.*)", i[1])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)  
                if source_2 in rec_c_qb:
                    rec_c_qb[source_2].append(filer)
                else:
                    rec_c_qb[source_2] = [filer]
                rec_c_qb_det[source_2]=[i[3]]
                rec_c_qb_det[source_2].append(i[9])
                rec_c_qb_det[source_2].append(i[10])  
                rec_c_qb_det[source_2].append(i[6])
            else:
                if i[1] in rec_c_qb:
                    rec_c_qb[i[1]].append(filer)
                else:
                    rec_c_qb[i[1]] = [filer]
                rec_c_qb_det[i[1]]=[i[3]] #Env
                rec_c_qb_det[i[1]].append(i[9]) #BUGF
                rec_c_qb_det[i[1]].append(i[10]) #App
                rec_c_qb_det[i[1]].append(i[6]) #Path
                    
    for key,value in rec_c_qb.items():
        if value  in rec_c_qb.values():
            rec_c_qb[key]=list(set(value))



    for k,v in rec_c_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_c_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_qdc_c_qb[k] = [filername] 
            rec_qdc_c_qb[k].append(k)
            rec_qdc_c_qb[k].append(rec_c_qb_det[k][2]) #App 
    
<<<<<<< HEAD
    #return rec_qdc_c_ops,rec_qdc_c_qb
    return OrderedDict(sorted(rec_qdc_c_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_qdc_c_qb.items(), key=lambda e: e[1][2])) #Ordered Dictionary by app name
=======
    return rec_qdc_c_ops,rec_qdc_c_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1


def getQDC_E_hf(filername):  
    recops = OpsInvData()   #OpsInv
    rec_e_qb={}   #Dict with Host as key and filer as list
    rec_e_qb_det = {}
    rec_e = {}
    rec_qdc_e_ops = {}
    rec_qdc_e_qb = {}
    out = open('QDC_E.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bjbg68zqs?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('QDC_E.csv','rU') 
    csv_r3 = csv.reader(qbData)
        
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_e:
                        rec_e[source_2].append(filer)  
                    else:
                        rec_e[source_2] = [filer] 
            else: 
                if i[2] in recops:
                    if i[2] in rec_e:
                        rec_e[i[2]].append(filer)
                    else:
                        rec_e[i[2]] = [filer]
                        
    for key,value in rec_e.items():
        if value  in rec_e.values():
            rec_e[key]=list(set(value))
            
    for k,v in rec_e.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_qdc_e_ops[k] = [filername] 
            rec_qdc_e_ops[k].append(k)
            rec_qdc_e_ops[k].append(recops[k][2])
            rec_qdc_e_ops[k].append(recops[k][1])#Env 
    
    qbData = open('QDC_E.csv','rU') 
    csv_r3 = csv.reader(qbData)
    for i in csv_r3:  
        if (i[9] == 'CTO'):
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)   
                if source_2 in rec_e_qb:
                    rec_e_qb[source_2].append(filer)
                else:
                    rec_e_qb[source_2] = [filer] 
                rec_e_qb_det[source_2]= [i[9]] # BUFG
                rec_e_qb_det[source_2].append(i[11]) #App
                rec_e_qb_det[source_2].append(i[6]) #Path
            else:
                if i[2] in rec_e_qb:
                    rec_e_qb[i[2]].append(filer)
                else:
                    rec_e_qb[i[2]] = [filer] 
                rec_e_qb_det[i[2]] = [i[9]]
                rec_e_qb_det[i[2]].append(i[11]) 
                rec_e_qb_det[i[2]].append(i[6])
                    
    for key,value in rec_e_qb.items():
        if value  in rec_e_qb.values():
            rec_e_qb[key]=list(set(value))


    for k,v in rec_e_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_e_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_qdc_e_qb[k] = [filername] 
            rec_qdc_e_qb[k].append(k)
            rec_qdc_e_qb[k].append(rec_e_qb_det[k][1]) #App   

    
<<<<<<< HEAD
    #return rec_qdc_e_ops,rec_qdc_e_qb
    return OrderedDict(sorted(rec_qdc_e_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_qdc_e_qb.items(), key=lambda e: e[1][2])) #Ordered Dictionary by app name
=======
    return rec_qdc_e_ops,rec_qdc_e_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1


def getLVDC_A_hf(filername):  
    recops = OpsInvData()   #OpsInv
    rec_a_lv_qb={}   #Dict with Host as key and filer as list
    rec_a_lv_qb_det = {}
    rec_a_lv = {}
    rec_lvdc_a_ops = {}
    rec_lvdc_a_qb = {}
    out = open('LVDC_A.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bhj3en5mh?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('LVDC_A.csv','rU') 
    csv_r3 = csv.reader(qbData)
        
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_a_lv:
                        rec_a_lv[source_2].append(filer)  
                    else:
                        rec_a_lv[source_2] = [filer] 
            else: 
                if i[2] in recops:
                    if i[2] in rec_a_lv:
                        rec_a_lv[i[2]].append(filer)
                    else:
                        rec_a_lv[i[2]] = [filer]
                        
    for key,value in rec_a_lv.items():
        if value  in rec_a_lv.values():
            rec_a_lv[key]=list(set(value))

    for k,v in rec_a_lv.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_lvdc_a_ops[k] = [filername] 
            rec_lvdc_a_ops[k].append(k)
            rec_lvdc_a_ops[k].append(recops[k][2])
            rec_lvdc_a_ops[k].append(recops[k][1])#Env 
    
    qbData = open('LVDC_A.csv','rU') 
    csv_r3 = csv.reader(qbData)
    
    for i in csv_r3:  
        if (i[8] == 'CTO'): 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)  
                if source_2 in rec_a_lv_qb:
                    rec_a_lv_qb[source_2].append(filer)
                else:
                    rec_a_lv_qb[source_2] = [filer] 
                rec_a_lv_qb_det[source_2]= [i[8]] # BUFG
                rec_a_lv_qb_det[source_2].append(i[9]) #App
                rec_a_lv_qb_det[source_2].append(i[5]) #Path
            else:
                if i[2] in rec_a_lv_qb:
                    rec_a_lv_qb[i[2]].append(filer)
                else:
                    rec_a_lv_qb[i[2]] = [filer] 
                rec_a_lv_qb_det[i[2]] = [i[8]]
                rec_a_lv_qb_det[i[2]].append(i[9]) 
                rec_a_lv_qb_det[i[2]].append(i[5])
                    
    for key,value in rec_a_lv_qb.items():
        if value  in rec_a_lv_qb.values():
            rec_a_lv_qb[key]=list(set(value))
   
    
    for k,v in rec_a_lv_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_a_lv_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_lvdc_a_qb[k] = [filername] 
            rec_lvdc_a_qb[k].append(k)
            rec_lvdc_a_qb[k].append(rec_a_lv_qb_det[k][1]) #App 

    
<<<<<<< HEAD
    #return rec_lvdc_a_ops,rec_lvdc_a_qb
    return OrderedDict(sorted(rec_lvdc_a_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_lvdc_a_qb.items(), key=lambda e: e[1][2]))
=======
    return rec_lvdc_a_ops,rec_lvdc_a_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1


def getLVDC_B_hf(filername):  
    recops = OpsInvData()   #OpsInv
    rec_b_lv_qb={}   #Dict with Host as key and filer as list
    rec_b_lv_qb_det = {}
    rec_b_lv = {}
    rec_lvdc_b_ops = {}
    rec_lvdc_b_qb = {}
    out = open('LVDC_B.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bjbg694f9?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''6''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'') 
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    qbData = open('LVDC_B.csv','rU') 
    csv_r3 = csv.reader(qbData) 
        
    for i in csv_r3: 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            if source: 
                source_2 = source.group(1)  
                if source_2 in recops: 
                    if source_2 in rec_b_lv:
                        rec_b_lv[source_2].append(filer)  
                    else:
                        rec_b_lv[source_2] = [filer] 
            else: 
                if i[2] in recops:
                    if i[2] in rec_b_lv:
                        rec_b_lv[i[2]].append(filer)
                    else:
                        rec_b_lv[i[2]] = [filer]
                        
    for key,value in rec_b_lv.items():
        if value  in rec_b_lv.values():
            rec_b_lv[key]=list(set(value))

    for k,v in rec_b_lv.items():
        if (filername in v) and (k in recops) and recops[k][1] == 'PRD':
            rec_lvdc_b_ops[k] = [filername] 
            rec_lvdc_b_ops[k].append(k)
            rec_lvdc_b_ops[k].append(recops[k][2])
            rec_lvdc_b_ops[k].append(recops[k][1])#Env 
    
    for i in csv_r3:  
        if (i[9] == 'CTO'): 
            source = re.search("(.*?)\.(.*)", i[2])
            filer_s = re.search("(.*?)\.(.*)", i[0])
            if filer_s:
                filer = filer_s.group(1)
            else:
                filer = i[0]
            
            if source:
                source_2 = source.group(1)  
                if source_2 in rec_b_lv_qb:
                    rec_b_lv_qb[source_2].append(filer)
                else:
                    rec_b_lv_qb[source_2] = [filer] 
                rec_b_lv_qb_det[source_2]= [i[9]] # BUFG
                rec_b_lv_qb_det[source_2].append(i[11]) #App
                rec_b_lv_qb_det[source_2].append(i[6]) #Path
            else:
                if i[2] in rec_b_lv_qb:
                    rec_b_lv_qb[i[2]].append(filer)
                else:
                    rec_b_lv_qb[i[2]] = [filer] 
                rec_b_lv_qb_det[i[2]] = [i[9]]
                rec_b_lv_qb_det[i[2]].append(i[11]) 
                rec_b_lv_qb_det[i[2]].append(i[6])
                    
    for key,value in rec_b_lv_qb.items():
        if value  in rec_b_lv_qb.values():
            rec_b_lv_qb[key]=list(set(value))
   
            
    for k,v in rec_b_lv_qb.items():
        #if k not in recops and (searchFiler in v) and (rec_b_lv_qb_det[k][0] =='Prod'): QDC A has no env col[Prod]
        if k not in recops and (filername in v):
            rec_lvdc_b_qb[k] = [filername] 
            rec_lvdc_b_qb[k].append(k)
            rec_lvdc_b_qb[k].append(rec_b_lv_qb_det[k][2]) #App 

    
<<<<<<< HEAD
    #return rec_lvdc_b_ops,rec_lvdc_b_qb
    return OrderedDict(sorted(rec_lvdc_b_ops.items(), key=lambda e: e[1][2])),OrderedDict(sorted(rec_lvdc_b_qb.items(), key=lambda e: e[1][2]))
=======
    return rec_lvdc_b_ops,rec_lvdc_b_qb
>>>>>>> Checked in pagerstats v1. Working drilldown 1



def getVfiler(filername):  
    vfiler = {}
    d_vfiler = {}
    out = open('vFiler.csv', "w")  
    req = urllib2.Request('https://intuitcorp.quickbase.com/db/bijddjssa?a=API_GenResultsTable&apptoken=77c6ty2v6kf5x3ndywbnag3cr&query={''7''.CT.'+filername+'}&options=csv&username='+username+'&password='+pwd+'')
    out.write(urllib2.urlopen(req).read()) 
    out.close() 
    vfiler_source = csv.reader(open('vFiler.csv','rU'))
    retFilerName = None
    
    for i in vfiler_source:
        vfiler_s = re.search("(.*?)\.(.*)", i[1])
        filer_s = re.search("(.*?)\.(.*)", i[2]) 
        if vfiler_s: vfiler = vfiler_s.group(1)
        else: vfiler = i[1]
        
        if filer_s: filer = filer_s.group(1)
        else: filer = i[2]
            
        if vfiler in d_vfiler:
            d_vfiler[vfiler].append(filer)
        else:
            d_vfiler[vfiler] = [filer]
            
    for key,value in d_vfiler.items():
        if value  in d_vfiler.values():
            d_vfiler[key]=list(set(value))
            
    
    for a,b in d_vfiler.items():
        if (filername == a) and (len(b) == 1):
            retFilerName = d_vfiler[a][0]
    if retFilerName:
        return retFilerName
    else:
        return "ERROR"








