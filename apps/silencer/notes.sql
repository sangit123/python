create table lookup (app_name varchar(200) ,app_group varchar(200) ,datacenter varchar(200) , hostnames varchar(200) , wily_alert varchar(200) , wily_mom varchar(200) , spectrum varchar(200) , sitescope varchar(200) , pagerduty varchar(200) , splunk varchar(200) , wily varchar(200) , newrelic varchar(200) )




LOAD DATA LOCAL INFILE 'application_host.csv' INTO TABLE pagerstats.silencer_app_service_details  FIELDS TERMINATED BY ','  LINES TERMINATED BY '\r' IGNORE 1 LINES (service_id,app_name, app_group,group_id,datacenter,hostnames,wily_alert,wily_mom,spectrum,sitescope,pagerduty,splunk,wily,newrelic);
