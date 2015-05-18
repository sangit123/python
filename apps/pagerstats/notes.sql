select source_date,str_to_Date(open_Date,'%Y-%m-%d')dd,shift from pagerstats_app_source_data;



select str_to_Date(open_Date,'%Y-%m-%d')dd,count(open_date)opendate from pagerstats_app_source_data group by str_to_Date(open_Date,'%Y-%m-%d');
select group_date,count(open_date)count from pagerstats_app_source_data group by group_date order by 1;


==wrong data
2015-04-21 |       76 |
| 2015-04-22 |        3


select group_date,count(open_date)count from pagerstats_app_source_data group by group_date order by 1;
select group_date,count(open_date)count from app_chart_source_data group by group_date order by 1;


==

select group_date,service_name,count(open_date)count from pagerstats_app_source_data group by group_date,service_name  order by 1;


http://jsfiddle.net/phpdeveloperrahul/FW64T/

http://stackoverflow.com/questions/24457486/highcharts-xaxis-drilldown-dont-change-correctly

http://jsfiddle.net/jugal/uhydP/ --- Pie percentage
http://jsfiddle.net/gh/get/jquery/1.9.1/highslide-software/highcharts.com/tree/master/samples/highcharts/demo/spline-plot-bands/ -- spline




alter table pagerstats_app_source_data drop primary key, add primary key(open_date, close_date);

select service_name,count(open_date) AS count from pagerstats_app_source_data group by service_name order by 2 desc;

from django.db import connection
cursor = connection.cursor()
cursor.execute("select service_name,count(open_date) AS count from pagerstats_app_source_data group by service_name order by 2 desc limit 5")
total_rows = cursor.fetchall()
[list(i) for i in total_rows]


fromdate = datetime.date.today() - datetime.timedelta(1)
todate = datetime.date.today() - datetime.timedelta(interval)

select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null group by group_date
union
select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null group by group_date order by 1;


select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date > '2015-05-02' and group_date < '2015-05-10') group by group_date
union
select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date > '2015-05-02' and group_date < '2015-05-10') group by group_date order by 1;




====12/05
select description,count(group_date)count from pagerstats_app_source_data group by description;

select description,group_date,count(group_date)count from pagerstats_app_source_data where description='"[API Gateway] Apache Availabi' and group_date >'2015-04-28' group by group_date,description order by 1;

select description,group_date,count(group_date)count,service_name from pagerstats_app_source_data where group_date >='2015-04-27' group by group_date,description,service_name order by 3 desc limit 3;

select service_name,count(open_date) AS count from pagerstats_app_source_data where group_date >= '2015-05-06' and group_date <= '2015-05-12' and shift in ('US','IDC') group by service_name order by 2 desc limit 5


==13/05
select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '2015-05-06' and group_date <= '2015-05-12') group by group_date
union
select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '2015-05-06' and group_date <= '2015-05-12') group by group_date order by 1



select group_date,count(open_date)count from pagerstats_app_source_data where domain is not null and service_name is not null and (group_date >= '2015-05-06' and group_date <= '2015-05-12') and shift in ('IDC') and domain in ('ICS' ) group by group_date
union 							
select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date >= '2015-05-06' and group_date <= '2015-05-12')  group by group_date order by 1




"select service_name,count(open_Date) from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and shift in ("+shift+") and domain in ("+ domain+" ) group by group_date"





select service_name,description,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-04-29' and group_date <= '2015-05-13') and shift in ('IDC') and domain in ('ICS' ))*100)avg,(count(open_Date)/15)noise_ratio from pagerstats_app_source_data where (group_date >= '2015-04-29' and group_date <= '2015-05-13') and shift in ('IDC') and domain in ('ICS' ) group by service_name,description order by 3 desc limit 5;

select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-04-29' and group_date <= '2015-05-13') and shift in ('IDC') and domain in ('ICS' );

select shift,count(open_Date)count,32 avg,round((count(open_Date)/15),1)noise_ratio from pagerstats_app_source_data where (group_date >= '2015-04-29' and group_date <= '2015-05-13')  and domain in ('ICS' ) group by shift;





insight_sql = "select shift,count(open_Date)count,32 avg,(count(open_Date)/+"+str(interval)+")noise_ratio from pagerstats_app_source_data where (group_date >= '"+str(fromdate)+"' and group_date <= '"+str(todate)+"') and domain in ("+ domain+" ) group by shift order by shift";


select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-05-07' and group_date <= '2015-05-14')  and domain in ('ICS' ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,"2wks" frequency from pagerstats_app_source_data where (group_date >= '2015-04-30' and group_date <= '2015-05-14') and domain in ('ICS' ) group by shift
union
select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-04-30' and group_date <= '2015-05-07')  and domain in ('ICS' ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,"4wks" frequency from pagerstats_app_source_data where (group_date >= '2015-04-15' and group_date <= '2015-05-14') and domain in ('ICS' ) group by shift
union
select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-04-01' and group_date <= '2015-05-14')  and domain in ('ICS' ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,"6wks" frequency from pagerstats_app_source_data where (group_date >= '2015-04-01' and group_date <= '2015-05-14') and domain in ('ICS' ) group by shift


===

select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-05-07' and group_date <= '2015-05-14')  and domain in ('ICS' ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,'2wks' frequency from pagerstats_app_source_data where (group_date >= '2015-04-30' and group_date <= '2015-05-14') and domain in ('ICS' ) group by shift
union 
select shift,count(open_Date)count,round(count(open_Date)/(select count(open_date)tt from pagerstats_app_source_data where (group_date >= '2015-04-30' and group_date <= '2015-05-07')  and domain in ('ICS' ))*100)avg,round((count(open_Date)/+15),2)noise_ratio,4wks frequency from pagerstats_app_source_data where (group_date >= '2015-04-15' and group_date <= '2015-05-14') and domain in ('ICS' ) group by shift


































































