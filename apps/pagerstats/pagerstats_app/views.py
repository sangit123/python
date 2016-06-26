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
from pagerstats_app.forms import PagerForm
from datetime import datetime
import datetime


def getData(request):
    interval=15
    error = False
    if request.method == 'GET': 
        
        form = PagerForm(request.GET)
        if form.is_valid(): 
            var = form.cleaned_data
            getShift = var['shift']
            getDomain = var['domain']
            #print getDomain
            if getShift == 'idc':
                shift = "'IDC'"
            elif getShift == 'us':
                shift = "'US'"
            elif getShift == 'total':
                shift = "'US','IDC'"
            else:
                shift = 'idc'

            if getDomain == 'ics':
                domain = "'ICS'"
            elif getDomain == 'pcs':
                domain = "'PCS'"
            elif getDomain == 'mobile':
                domain = "'MOBILE'" 
            elif getDomain == 'fds':
                domain = "'FDS'"
            else:
                domain = "'ICS'"




            #out = open('/root/python_proj/apps/pagerstats/pagerstats_app/logs.csv', 'a') 
            out = open('/Users/shaveri/python/apps/pagerstats/pagerstats_app/logs.csv', 'a') 
            out.write(domain+","+str(datetime.datetime.now()))
            out.write('\n')
            out.close



            #To check whether data already present in DB 
            interval_api = None
            total_rows = []
            v_count_sql = "select DATEDIFF(CURDATE(),DATE_SUB(max(group_date),INTERVAL 2 DAY))interval_days from pagerstats_app_source_data where domain in ("+ domain+" ) ;"
            cursor = connection.cursor()
            cursor.execute(v_count_sql)
            total_rows = cursor.fetchall()
            interval_api = total_rows[0][0]
            if interval_api == 0 or interval_api is None:
                interval_api = 15

            for i in (datetime.date.today() - datetime.timedelta(n-1)  for n in range(interval_api)): 
                fromdate = (i - datetime.timedelta(days=1))
                get_incidents(fromdate,i,domain)

            #To fill 'no incident data'
            todate = datetime.date.today() - datetime.timedelta(0)
            fromdate = datetime.date.today() - datetime.timedelta(interval)
            cursor = connection.cursor()
            cursor.execute("select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date\
                            union \
                            select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') group by group_date order by 1")
                
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            no_incident = []
            for i in li: 
                no_incident.append(i[0].strftime("%m-%d-%Y"))
            
            #print no_incident
            for i in (datetime.date.today() - datetime.timedelta(n-1) for n in range(interval)): 
                fromdate = (i - datetime.timedelta(days=1))
                no_incident_date = str(fromdate.strftime("%m-%d-%Y"))
                if no_incident_date not in no_incident:
                    no_incident_date = format_date(fromdate)
                    p=Source_data(source_date=no_incident_date,open_date=str(no_incident_date),close_date=no_incident_date,create_date=datetime.datetime.now(),group_date=no_incident_date)
                    p.save()
            cursor.close()

            #Weekly service data
            data_source_wk = []
            todate = datetime.date.today() - datetime.timedelta(0)
            fromdate = datetime.date.today() - datetime.timedelta(interval)
            cursor = connection.cursor()
            cursor.execute("select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ) group by group_date\
                            union \
                            select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" )  group by group_date order by 1")
            

            incident_sql = "select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ) group by group_date\
                            union \
                            select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"')  group by group_date order by 1;"
            #print incident_sql
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li: 
                temp = {} 
                temp['group_date'] = i[0].strftime("%m-%d-%Y")
                temp['total'] = int(i[1]) 
                temp['drill'] = int(i[0].strftime("%m%d%Y"))
                data_source_wk.append(temp)
            cursor.close() 
            

            #Daily service data[for Drilldown line chart]
            data_source_dly = [] 
            cursor = connection.cursor()
            cursor.execute("select group_date,service_name,count(open_date)count from pagerstats_app_source_data  where shift in ("+shift+") and domain in ("+ domain+" ) group by group_date,service_name  order by 1")
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li: 
                temp = {} 
                temp['group_date'] = i[0].strftime("%m-%d-%Y")
                temp['service_name'] = str(i[1])
                temp['total'] = i[2]
                temp['drill'] = int(i[0].strftime("%m%d%Y"))
                data_source_dly.append(temp)
            cursor.close()
            #print data_source_dly


            #pie chart data
            service_count_wk_pie = [] 
            cursor = connection.cursor()
            cursor.execute("select service_name,count(open_date) AS count from pagerstats_app_source_data where group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"' and shift in ("+shift+") and domain in ("+ domain+" )group by service_name order by 2 desc limit 5")
            #print_sql = "select service_name,count(open_date) AS count from pagerstats_app_source_data where group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"' and shift in ("+shift+") and domain in ("+ domain+" )group by service_name order by 2 desc limit 5"
            #print print_sql
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li: 
                temp = {}
                temp ['service_name'] = str(i[0])
                temp ['count'] = int(i[1]) 
                service_count_wk_pie.append(temp)
            #print service_count_wk_pie

            #insights
            insights_data = []
            cursor = connection.cursor()
            insight_sql = "select service_name,description,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+"+str(interval)+"),2)noise_ratio from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ) group by service_name,description order by 3 desc limit 5";
            #print insight_sql
            cursor.execute(insight_sql)
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li: 
                temp = {}
                temp ['service_name'] = str(i[0])
                temp ['description'] = i[1]
                temp ['count'] = int(i[2]) 
                temp ['avg'] = int(i[3])
                temp ['noise_ratio'] = i[4]
                insights_data.append(temp)
            cursor.close()
            #print insights_data

            #Shift Status
            shift_data = []
            cursor = connection.cursor()
            insight_sql = "select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+"+str(interval)+"),2)noise_ratio from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and domain in ("+ domain+" ) group by shift order by shift";
            #insight_sql = "select shift,count(open_Date)count,32 avg,(count(open_Date)/+"+str(interval)+")noise_ratio from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and domain in ("+ domain+" ) group by shift order by shift"
            #print insight_sql
            cursor.execute(insight_sql)
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li:
                temp = {}
                temp ['shift'] = str(i[0])
                temp ['count'] = i[1]
                temp ['avg'] = int(i[2]) 
                temp ['noise_ratio'] = i[3]
                shift_data.append(temp)
            cursor.close()
            
            #Noise Pulse
            noise_pulse = []
            cursor = connection.cursor()
            noise_pulse_sql = "select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=7))+"' and group_date <= '"+str(todate)+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+str(todate)+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=7))+"' and group_date <= '"+str(todate)+"') and domain in ("+ domain+" )and shift in ("+shift+") group by frequency \
                          union \
                          select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=14))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=7))+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+ str(todate  - datetime.timedelta(days=7))+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=14))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=7))+"') and domain in ("+ domain+" ) and shift in ("+shift+") group by frequency \
                          union \
                          select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=21))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=14))+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+ str(todate  - datetime.timedelta(days=14))+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=21))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=14))+"') and domain in ("+ domain+" ) and shift in ("+shift+") group by frequency \
                          union \
                          select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=28))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=21))+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+ str(todate  - datetime.timedelta(days=21))+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=28))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=21))+"') and domain in ("+ domain+" ) and shift in ("+shift+") group by frequency \
                          union \
                          select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=35))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=28))+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+ str(todate  - datetime.timedelta(days=28))+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=35))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=28))+"') and domain in ("+ domain+" ) and shift in ("+shift+") group by frequency \
                          union \
                          select count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=42))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=35))+"')  and domain in ("+ domain+" ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'"+ str(todate  - datetime.timedelta(days=35))+"' frequency from pagerstats_app_source_data where (group_date >= '"+str(todate  - datetime.timedelta(days=42))+"' and group_date <= '"+str(todate  - datetime.timedelta(days=35))+"') and domain in ("+ domain+" ) and shift in ("+shift+") group by  frequency order by 4;"
            cursor.execute(noise_pulse_sql)
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li:
                temp = {}
                #temp ['shift'] = str(i[0])
                temp ['count'] = i[0]
                temp ['avg'] = int(i[1]) 
                temp ['noise_ratio'] = i[2]
                temp ['frequency'] = str(i[3])
                #temp ['frequency'] = datetime.datetime.strptime(i[4],"%Y-%m-%d")
                noise_pulse.append(temp)
            cursor.close()
            #print noise_pulse_sql

            alert_summary = []
            #alert_desc_dd = []
            cursor = connection.cursor()
            alert_summary_sql = "select open_date,substr(dayname(open_date),1,3)day,service_name,shift,description,resolved_by,domain from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ) order by 1 desc;"
            #print alert_summary_sql
            cursor.execute(alert_summary_sql)
            total_rows = cursor.fetchall()
            li=[list(i) for i in total_rows]
            for i in li:
                temp = {}
                temp ['open_date'] = i[0]
                temp ['day'] = i[1]
                temp ['service_name'] = i[2]
                temp ['shift'] = i[3]
                temp ['description'] = i[4]
                temp ['resolved_by'] = i[5]
                temp ['domain'] = i[6]
                alert_summary.append(temp)
            cursor.close()
            #print alert_desc_dd_sql
            #alert_desc_sql="select open_date,service_name,description,shift,resolved_by from pagerstats_app_source_data where group_date= '2015-05-14' and domain='ICS' and shift='IDC' order by 1;"



            domain = domain.strip("''") 
            return render(request, 'results.html', {'data_source_wk': data_source_wk,'data_source_dly':data_source_dly,'service_count_wk_pie':service_count_wk_pie,'form': form,'insights_data':insights_data,'shift_data':shift_data,'domain':domain,'noise_pulse':noise_pulse,'alert_summary':alert_summary})
        else: 
            return render(request,'search_form.html', {'form': form,'error':error})
    else:
        print "Errror sir"
        error = False
        form = PagerForm(request.GET)
        return render(request,'search_form.html', {'form': form,'error':error})

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
    if domain == "'ICS'":
        API_ACCESS_KEY = API_ACCESS_KEY_ICS
        SUBDOMAIN = SUBDOMAIN_ICS
    elif domain == "'PCS'":
        API_ACCESS_KEY = API_ACCESS_KEY_PCS
        SUBDOMAIN = SUBDOMAIN_PCS
    elif domain == "'MOBILE'":
        API_ACCESS_KEY = API_ACCESS_KEY_MOBILE
        SUBDOMAIN = SUBDOMAIN_MOBILE
    elif domain == "'FDS'":
        API_ACCESS_KEY = API_ACCESS_KEY_FDS
        SUBDOMAIN = SUBDOMAIN_FDS
    else:
        API_ACCESS_KEY = None
        SUBDOMAIN = None
    domain = domain.strip("''") 

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
    description = None
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
            resolved_by = key['resolved_by_user']['name']
            closed_on = key['last_status_change_on']
            escalations = key['number_of_escalations']
            description = key['trigger_summary_data']['description'][0:40]
            
            
        except KeyError:    
            try:
                description = key['trigger_summary_data']['subject'][0:40]
            except:
                pass
        except TypeError:
            resolved_by = None
            pass
        
        


    
        #print str(key['created_on'])+"    "+str(psttime_open)+"    "+shift+"    "+service_name+"    "+description
        p=Source_data(source_date=utc,open_date=str(psttime_open),close_date=psttime_close,service_name=service_name,shift=shift,description=description,resolved_by=resolved_by,escalations=escalations,create_date=datetime.datetime.now(),group_date=group_date,domain=domain)
        p.save()



  

