
import numpy as np;
import pandas as pd;
from datetime import datetime
import psycopg2
from datetime import date
import time
import math



date_format = "%Y-%m-%d %H:%M:%S"

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

#changer apres pour la config definitif
spool = { 'tsm_tlsp1' : config2,
          'tsm_tlsp2' : config2,
          'jsapp'     : config1,
          'dbgnrtmil' : config1}


def create_dataframe(name, spooler, conf, lim=100000):
    #spooler = conf['spooler'];
    #try:
    conn = psycopg2.connect("dbname='"+conf['dbname']+"' user='"+conf['user']+"' host='"+conf['host']+"' password='"+conf['password']+"'");
    if(name != None):
        df = pd.read_sql_query('select * from scheduler_history as sh where sh."JOB_NAME" = \''+name+'\' and sh."SPOOLER_ID" =\''+spooler+'\' limit '+str(lim)+';',con=conn)
        tab = []
        for i in range(0, len(df)):
            epoch1 = int(time.mktime(time.strptime(str(df['START_TIME'][i]), date_format)));
            epoch2 = int(time.mktime(time.strptime(str(df['END_TIME'][i]), date_format)));
            tab.append(epoch2 - epoch1)
        serie = pd.Series(tab)
        df['duration'] = serie;
    else:
        df = pd.read_sql_query('select * from scheduler_history as sh limit '+str(lim)+';',con=conn)
        #print("connection: ok")
    conn.close();
    return df;
    #except:
    #    print("I am unable to connect to the database");



def produce_box(df):
    dfp = pd.DataFrame(df, columns=[ 'duration', 'JOB_NAME'])
    bp = dfp.boxplot( by='JOB_NAME', return_type='dict')
    #dfp.boxplot( by='JOB_NAME', return_type='dict');
    print bp.keys();
    print bp['duration']['boxes']
    fig = bp['duration']['boxes'][0].get_figure()
    return fig;


def filter_date(df, start_date, end_date):
    mask = (df['START_TIME'] > start_date) & (df['START_TIME'] <= end_date);
    return df.loc[mask];


def dfDescribe2xml(df):
    'Pour le tableau de stat'
    n = df['ID'].size;
    arr1 = ['STEPS', 'duration'];
    arr = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows>";
    for i in range(0, 2):
        str1 += '<row id="'+arr1[i]+'">';
        str1 += '<cell>'+arr1[i]+'</cell>';
        for j in range(0, 8):
            #str1 += '<cell>'+arr[j]+'</cell>';
            str1 += '<cell>'+str(df[arr1[i]][arr[j]])+'</cell>';
        str1 += '</row>'
    str1 += '</rows>';
    return str1;


def df2xml(df):
    ''
    n    = df.index.size;
    m    = df.columns.size;
    arr1 = df.index;
    arr2 = df.columns;
    str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows>";
    for i in range(0, n):
        str1 += '<row id="'+str(df[arr2[0]][arr1[i]])+'">';
        for j in range(0, m):
            #str1 += '<cell>'+arr2[j]+'</cell>';
            str1 += '<cell>'+str(df[arr2[j]][arr1[i]])+'</cell>';
        str1 += '</row>'
    str1 += '</rows>';
    return str1;





def df2xml1(df):
    'Pour le grid de job'
    n    = df.describe()['ID'].size
    arr1 = df.index;
    arr2 = ['ID', 'JOB_NAME']
    str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows>";
    for i in range(0, n):
        str1 += '<row id="'+str(arr1[i])+'">';
        for j in range(0, 2):
            #str1 += '<cell>'+arr2[j]+'</cell>';
            str1 += '<cell>'+str(df[arr2[j]][arr1[i]])+'</cell>';
        str1 += '</row>'

    str1 += '</rows>';
    return str1;




def anomaly(df):
    'from dataframe found patological cases'
    max1 = df.describe().loc['75%']['duration']
    if(math.isnan(max1)):
        return pd.DataFrame()
    else:
        query = 'duration > '+str(max1)
        tmp = pd.DataFrame(df.query(query), columns=['ID', 'START_TIME', 'CAUSE', 'duration']);
        return tmp;



def anomalyByDate(df, start_date, end_date):
    return anomaly(filter_date(df, start_date, end_date))
