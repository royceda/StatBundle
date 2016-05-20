
#import sys;



#from AriiStat import *
#name = 'tsm/af/fs/prd/TLSPBLDDWH02/allfs.incr.02.arc_logsar.scr';
#spooler = 'tsm_tlsp1';

name = str(sys.argv[1]);
spooler = sys.argv[2];



config = spool[spooler];
df = create_dataframe(name, config);

print "toto";
#print1();

#f = open('../views/tempChart/gridStat.xml.twig', 'w')
#f.write(dfDescribe2xml(df.describe()))
#f.close()
#print dfDescribe2xml(df.describe())



#cmd:  python dfDescribe2xml.py name spooler || date1 date2
