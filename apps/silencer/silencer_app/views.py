from django.http import HttpResponseRedirect 
from django.shortcuts import render 
from datetime import datetime
import datetime
from silencer_app.forms import SilencerForm
from silencer_app.models import service_details
from django.db import connection
import requests
import json 
from collections import Counter,OrderedDict

def getData(request):

	if request.method == 'GET' and 'getservicenames' not in request.GET:
		form = SilencerForm(request.GET)
		print form
		if form.is_valid():
			var = form.cleaned_data

			appgroup_drpdn_sql = "select distinct app_group from silencer_app_service_details union select ' Select App Group' as app_group from silencer_app_service_details order by app_group ;"
			print appgroup_drpdn_sql
			cursor = connection.cursor()
			cursor.execute(appgroup_drpdn_sql)
			total_rows = cursor.fetchall()
			print total_rows
			app_drpdn_data = []
			li=[list(i) for i in total_rows]
			for i in li:
				temp = {}
				temp['app_group'] = str(i[0])
				app_drpdn_data.append(temp)
				cursor.close()
			#service_names = getServiceDetails('ICS1')
			service_names = 0
			return render(request, 'results.html', {'form': form,'app_drpdn_data':app_drpdn_data,'service_names':service_names})

		else:
			appgroup_drpdn_sql = "select distinct app_group from silencer_app_service_details union select ' Select App Group' as app_group from silencer_app_service_details order by app_group ;"
			print appgroup_drpdn_sql
			cursor = connection.cursor()
			cursor.execute(appgroup_drpdn_sql)
			total_rows = cursor.fetchall()
			print total_rows
			app_drpdn_data = []
			li=[list(i) for i in total_rows]
			for i in li:
				temp = {}
				temp['app_group'] = str(i[0])
				app_drpdn_data.append(temp)
				cursor.close()
			return render(request, 'index.html', {'form': form,'app_drpdn_data':app_drpdn_data})
	elif request.method == 'GET' and 'getservicenames' in request.GET: #this parameter comes from submit type from view index
		form = SilencerForm(request.GET) 
		appgroup_drpdn_sql = "select distinct app_group from silencer_app_service_details union select ' Select App Group' as app_group from silencer_app_service_details order by app_group ;"
		print appgroup_drpdn_sql
		cursor = connection.cursor()
		cursor.execute(appgroup_drpdn_sql)
		total_rows = cursor.fetchall()
		print total_rows
		app_drpdn_data = []
		li=[list(i) for i in total_rows]
		for i in li:
			temp = {}
			temp['app_group'] = str(i[0])
			app_drpdn_data.append(temp)
			cursor.close()
		service_names,service_count = getServiceDetails('ICS')
		#service_names = None
		return render(request, 'results.html', {'form': form,'app_drpdn_data':app_drpdn_data,'service_names':service_names,'service_count':service_count})






def getServiceDetails(domain):
	service_data = {}
	if domain == "ICS":
		print "i am here in ICD block"
		API_ACCESS_KEY = '4vSp3jL1aYfNEeKEwWGT'
		SUBDOMAIN = 'ics-intuit'
		
		headers = {
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    	}
    	
    	count = [0,100,200,300,400,500]
    	for i in count:
	    	payload = {
	    	'offset' : i,'limit' : 100
	    	#'since': format_date(fromdate),'until': format_date(todate)
	    	#'status':'triggered,acknowledged,resolved','since': format_date(since),'until': format_date(until)
	    	#, 'fields':'incident_number,service,created_on,trigger_summary_data'
	    	}
	    	r = requests.get(
	            'https://{0}.pagerduty.com/api/v1/services'.format(SUBDOMAIN),
	            headers=headers,
	            params=payload,
	    	)
	    	output_json = json.loads(r.text)
	    	#print r.text
	    	#print i
	    	for key in output_json['services']:
	        	service_name = str(key['name'])
	        	service_key = str(key['service_key'])
	        	status = str(key['status'])
	        	service_id = str(key['id'])
	        	service_data[service_name] = [service_name]
	        	service_data[service_name].append(service_key)
	        	service_data[service_name].append(status)
	        	service_data[service_name].append(service_id)
	        #for key in output_json['services']:
	        #	temp = {}
            #    temp ['service_name'] = str(key['name'])
            #    temp ['service_key'] = str(key['service_key'])
            #    temp ['status'] = str(key['status'])
            #    service_data.append(temp)
		print len(service_data)

		service_data = OrderedDict(sorted(Counter(service_data).items()))
		service_count = len(service_data)

    	return service_data,service_count
	    
    	
	        
	        
	        
	         
	            
	            
	            
	        
	        
    	
    		