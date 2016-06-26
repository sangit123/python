import subprocess
import re
import os.path
ENVIRONMENT = 'PTE Testing';
PARAM_FILE_BASE = '/home/oracle/test_stats/params.prm';
GGSCI_BIN = '/u01/app/ogg/12.1.2.1.0/ggsci';

CMD='STATS REPLICAT RLPTE_D, LATEST,TOTALSONLY *.*, RESET\ninfo replicat RLPTE_D';
f = open(PARAM_FILE_BASE,'w')
f.write(CMD)
f.close()

proc = subprocess.Popen([GGSCI_BIN, "PARAMFILE",PARAM_FILE_BASE], stdout=subprocess.PIPE)
out, err = proc.communicate()

#print out
#print "=========="

output = out
stats = {}
for i in out.split('\n'):
    i = i.rstrip()
    grp = re.search("Sending STATS request to REPLICAT (.*) ...", i)
    if grp:
        group = (grp.group(1))

    ops = re.search("No database operations have been performed.",i)
    if ops:
        stats['Tot_Ops ']= 0
        stats['Inserts ']=0
        stats['Updates ']=0
        stats['Deletes ']=0


    ops = re.search("No active replication maps.",i)
    if ops:
        Total_ops = 0
        stats[group]=Total_ops

    ops = re.search("Total operations (.*).(00)",i)
    if ops:
        Total_ops = int(float(ops.group(1).lstrip().rstrip()))
        stats['Tot_Ops ']=Total_ops

    datetime = re.search("Start of Statistics at (.*) (.*):(.*).",i)
    if datetime:
        date = datetime.group(1)
        time = datetime.group(2)


    ops = re.search("Total inserts (.*).(00)",i)
    if ops:
        grp_insert = "Inserts "
        Total_inserts = int(float(ops.group(1).lstrip().rstrip()))
        stats[grp_insert]=Total_inserts
    #    print "Total_inserts :"+str(Total_inserts)

    ops = re.search("Total updates (.*).(00)",i)
    if ops:
        grp_update = "Updates "
        Total_updates = int(float(ops.group(1).lstrip().rstrip()))
        stats[grp_update]=Total_updates

    ops = re.search("Total deletes (.*).(00)",i)
    if ops:
        grp_update = "Deletes "
        Total_deletes = int(float(ops.group(1).lstrip().rstrip()))
        stats[grp_update]=Total_deletes

    chk_lag = re.search("Checkpoint Lag (.*)\((.*)",i)
    if chk_lag:
        lag = chk_lag.group(1)
        stats['Lag     '] = lag.lstrip().rstrip()





#Get the each group head with item value as list
groups_kv = stats.items()
#Get the file header for the stats
header = 'TIME_END '+' '.join(stats.keys())
#print header



out_file = "stats_report_"+date+".txt"

if not os.path.exists(out_file):
    #file(out_file).close()
    report = open(out_file, "w")
    report.write(header)
    report.write('\n')
    report.write("%-9s" % time)
    for k, v in groups_kv:
        report.write("%-9s" % v)
    report.close()
else:
    report = open(out_file, "a")
    report.write('\n')
    report.write("%-9s" % time)
    for k, v in groups_kv:
        report.write("%-9s" % v)
    report.close()