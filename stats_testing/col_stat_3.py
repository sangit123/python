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

v_total = ()
v_insert = ()
v_delete = ()
v_update = ()
v_lag = ()

#print out
#print "=========="

for i in out.split('\n'):
    i = i.rstrip()
    grp = re.search("Sending STATS request to REPLICAT (.*) ...", i)
    if grp:
        replicat = (grp.group(1))

    ops = re.search("No database operations have been performed.",i)
    if ops:
        Total_ops = 0
        v_total = ('Tot_Ops ',0)
        v_lag = ('Lag     ',0)
        v_insert = ('Inserts ',0)
        v_update = ('Updates ',0)
        v_delete = ('Deletes ',0)


    ops = re.search("No active replication maps.",i)
    if ops:
        Total_ops = 0
        v_total = ('Tot_Ops ',Total_ops)

    ops = re.search("Total operations (.*).(00)",i)
    if ops:
        Total_ops = int(float(ops.group(1).lstrip().rstrip()))
        v_total = ('Tot_Ops ',Total_ops)

    datetime = re.search("Start of Statistics at (.*) (.*):(.*).",i)
    if datetime:
        date = datetime.group(1)
        time = datetime.group(2)


    ops = re.search("Total inserts (.*).(00)",i)
    if ops:
        grp_insert = "Inserts "
        Total_inserts = int(float(ops.group(1).lstrip().rstrip()))
        v_insert = ('Inserts ',Total_inserts)

    ops = re.search("Total updates (.*).(00)",i)
    if ops:
        grp_update = "Updates "
        Total_updates = int(float(ops.group(1).lstrip().rstrip()))
        v_update = ('Updates ',Total_updates)

    ops = re.search("Total deletes (.*).(00)",i)
    if ops:
        grp_update = "Deletes "
        Total_deletes = int(float(ops.group(1).lstrip().rstrip()))
        v_delete = ('Deletes ',Total_deletes)

    chk_lag = re.search("Checkpoint Lag (.*)\((.*)",i)
    if chk_lag:
        lag = chk_lag.group(1)
        v_lag = ('Lag     ',lag.lstrip().rstrip())

dataset = []
dataset.append(v_lag)
dataset.append(v_total)
dataset.append(v_insert)
dataset.append(v_update)
dataset.append(v_delete)


#Get the file header for the stats
header = 'TIME_END '+'Lag      '+'Tot_Ops  '+'Inserts  '+'Updates  '+'Deletes  '


out_file = "OGG_stats_"+replicat+date+".txt"

if not os.path.exists(out_file):
    #file(out_file).close()
    report = open(out_file, "w")
    report.write(header)
    report.write('\n')
    report.write("%-9s" % time)
    for k, v in dataset:
        report.write("%-9s" % v)
    report.close()
else:
    report = open(out_file, "a")
    report.write('\n')
    report.write("%-9s" % time)
    for k, v in dataset:
        report.write("%-9s" % v)
    report.close()