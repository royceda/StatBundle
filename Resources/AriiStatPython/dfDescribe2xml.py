import sys
from AriiStat import *

config1 = { 'dbname'   : 'jsapp',
            'user'     : 'arii',
            'host'     : 'lh-cjsapp01-db',
            'password' : 'visuonly',
            'spooler'  : 'jsapp'}


config2 = { 'host'     : 'tlspnbdpgr02',
            'dbname'   : 'jstech',
            'user'     : 'arii',
            'password' : 'visuonly',
            'spooler'  : 'tsm_tlsp1'}


spool = { 'tsm_tlsp1' : config2,
          'tsm_tlsp2' : config2,
          'jsapp'     : config1}



#name = 'tsm/af/fs/prd/TLSPBLDDWH02/allfs.incr.02.arc_logsar.scr';
#print "aaa"
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

name = str(sys.argv[1]);
spooler = sys.argv[2];

config = spool[spooler];
df = create_dataframe(name, config);

f = open('../views/tempChart/gridStat.xml.twig','w')
f.write(dfDescribe2xml(df.describe()))
f.close()
