from django.http import HttpResponseRedirect 
from django.shortcuts import render 
from pagerstats_app.models import Source_data
from django.db.models import Count
from django.shortcuts import render 
import requests
import json  
from conf import *
import datetime
from dateutil import tz
import collections 
from django.shortcuts import render
from django.http import HttpResponse 
import csv   
from django.http import HttpResponseRedirect
from django.db import connection


def getData(request,interval=7): 
        for i in (datetime.date.today() - datetime.timedelta(n) for n in range(interval)): 
            fromdate = (i - datetime.timedelta(days=1))
            #get_incidents(fromdate,i,'ICS')

        #To fill no incident data
        todate = datetime.date.today() - datetime.timedelta(1)
        fromdate = datetime.date.today() - datetime.timedelta(interval)
        cursor = connection.cursor()
        cursor.execute("select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date\
						union\
						select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date order by 1")
        total_rows = cursor.fetchall()
        li=[list(i) for i in total_rows]
        no_incident = []
        for i in li: 
            no_incident.append(i[0].strftime("%m-%d-%Y"))
        
        #print no_incident
        for i in (datetime.date.today() - datetime.timedelta(n) for n in range(interval)): 
            fromdate = (i - datetime.timedelta(days=1))
            no_incident_date = str(fromdate.strftime("%m-%d-%Y"))
            if no_incident_date not in no_incident:
            	no_incident_date = format_date(fromdate)
            	p=Source_data(source_date=no_incident_date,open_date=str(no_incident_date),close_date=no_incident_date,create_date=datetime.datetime.now(),group_date=no_incident_date)
            	p.save()

        #Weekly service data
        data_source_wk = []
        todate = datetime.date.today() - datetime.timedelta(1)
        fromdate = datetime.date.today() - datetime.timedelta(interval)
        cursor = connection.cursor()
        cursor.execute("select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date\
						union\
						select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date order by 1")
        total_rows = cursor.fetchall()
        li=[list(i) for i in total_rows]
        for i in li: 
            temp = {} 
            temp['group_date'] = i[0].strftime("%m-%d-%Y")
            temp['total'] = int(i[1]) 
            temp['drill'] = int(i[0].strftime("%m%d%Y"))
            data_source_wk.append(temp) 
        

        #Daily service data[for Drilldown line chart]
        data_source_dly = [] 
        cursor = connection.cursor()
        cursor.execute("select group_date,service_name,count(open_date)count from pagerstats_app_source_data group by group_date,service_name  order by 1")
        total_rows = cursor.fetchall()
        li=[list(i) for i in total_rows]
        for i in li: 
            temp = {} 
            temp['group_date'] = i[0].strftime("%m-%d-%Y")
            temp['service_name'] = str(i[1])
            temp['total'] = i[2]
            temp['drill'] = int(i[0].strftime("%m%d%Y"))
            data_source_dly.append(temp)
        #print data_source_dly


        #pie chart data
        service_count_wk_pie = [] 
        cursor = connection.cursor()
        cursor.execute("select service_name,count(open_date) AS count from pagerstats_app_source_data where group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"' group by service_name order by 2 desc limit 5")
        total_rows = cursor.fetchall()
        li=[list(i) for i in total_rows]
        for i in li: 
            temp = {}
            temp ['service_name'] = str(i[0])
            temp ['count'] = int(i[1]) 
            service_count_wk_pie.append(temp)
        #print service_count_wk_pie

	return render(request, 'results.html', {'data_source_wk': data_source_wk,'data_source_dly':data_source_dly,'service_count_wk_pie':service_count_wk_pie}) 


def format_date(date):
    return date.strftime("%Y-%m-%d")


def get_incidents(fromdate,todate,domain): 
    fmt = "%Y-%m-%dT%H:%M:%SZ" 
    fmt_time = '%H:%M:%S'
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('US/Pacific') 
    service_count = {}  
    fr = datetime.datetime.strptime('06:00:00','%H:%M:%S')
    to = datetime.datetime.strptime('18:00:00','%H:%M:%S')
    if domain == 'ICS':
        API_ACCESS_KEY = API_ACCESS_KEY_ICS
        SUBDOMAIN = SUBDOMAIN_ICS
    headers = {
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    }
    payload = {
        'since': format_date(fromdate),'until': format_date(todate)
        #'status':'triggered,acknowledged,resolved','since': format_date(since),'until': format_date(until)
        #, 'fields':'incident_number,service,created_on,trigger_summary_data'
    }
    r = requests.get(
                    'https://{0}.pagerduty.com/api/v1/incidents'.format(SUBDOMAIN),
                    headers=headers,
                    params=payload,
    )  
    #print r.text
    output_json = json.loads(r.text) 
    
    resolved_by = None
    escalations = None
    group_date = None
    for key in output_json['incidents']:
        utctime = str(key['created_on'])
        utc = datetime.datetime.strptime(utctime, fmt)
        utc = utc.replace(tzinfo=from_zone) 
        psttime_open = utc.astimezone(to_zone) 
        cen =datetime.datetime.strptime(psttime_open.strftime("%H:%M:%S"), fmt_time)


        psttime_close = key['last_status_change_on'] 
        utc_close = datetime.datetime.strptime(psttime_close, fmt)
        utc_close = utc_close.replace(tzinfo=from_zone) 
        psttime_close = utc_close.astimezone(to_zone)  
        group_date = format_date(psttime_open)
        #no_incident.append(group_date)
        
        try:
            if (cen > fr) and (cen < to ): 
                shift = 'US'
            else:
                shift = 'IDC'
                
            service_name = key['service']['name'] 
            description = key['trigger_summary_data']['description'][0:30]
            resolved_by = key['resolved_by_user']['name']
            closed_on = key['last_status_change_on']
            escalations = key['number_of_escalations']
            
            
        except KeyError:
            description = key['trigger_summary_data']['subject'][0:30]
            pass
        except TypeError:
            resolved_by = None
            pass
    
        #print str(key['created_on'])+"    "+str(psttime_open)+"    "+shift+"    "+service_name+"    "+description
        p=Source_data(source_date=utc,open_date=str(psttime_open),close_date=psttime_close,service_name=service_name,shift=shift,description=description,resolved_by=resolved_by,escalations=escalations,create_date=datetime.datetime.now(),group_date=group_date,domain=domain)
        p.save()



  

