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
select group_date,0 count from pagerstats_app_source_data where domain is null and service_name is null and (group_date > '2015-05-02' and group_date < '2015-05-10') group by group_date order by 1