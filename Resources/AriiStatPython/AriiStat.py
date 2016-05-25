
import numpy as np;
import pandas as pd;
from datetime import datetime
import psycopg2
from datetime import date
import time
import math


date_format = "%Y-%m-%d %H:%M:%S"

#depuis 2014
#jsapp
jsapp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 218306, 92897, 116148, 114403, 132307, 529814, 110530, 11478, 15428, 14814, 24933, 54482, 40730, 15862, 0, 0, 0, 0, 0, 0, 0]


#tsm_tlsp1: l'obtention est trop longue pour le notebook
tsm_tlsp1 = [0, 0, 0, 2328, 23361, 183242, 385607, 418031, 399328, 411786, 400016, 404987, 410094, 375845, 410611, 408610, 434860, 408772, 423007, 448903, 429273, 455137, 430230, 455221, 475069, 456360, 492839, 458865, 173785, 0, 0, 0, 0, 0, 0, 0]


#tsm_tlsp2: l'obtention est trop longue pour le notebook
tsm_tlsp2=[0, 0, 0, 1704, 16306, 16779, 278894, 304559, 304290, 327167, 324517, 337017, 348491, 321196, 359922, 359322, 379894, 376229, 399152, 408389, 400433, 426923, 427722, 446968, 499442, 496017, 544427, 530293, 210679, 0, 0, 0, 0, 0, 0, 0]


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
    try:
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
        return df;
    except:
        print("I am unable to connect to the database");


def produce_box(df):
    dfp = pd.DataFrame(df, columns=[ 'duration', 'JOB_NAME'])
    bp = dfp.boxplot( by='JOB_NAME', return_type='dict')
    #dfp.boxplot( by='JOB_NAME', return_type='dict');
    print bp.keys();
    print bp['duration']['boxes']
    fig = bp['duration']['boxes'][0].get_figure()
    return fig;


def filter_date(df, start_date, end_date):
    mask = (df['START_TIME'] >= start_date) & (df['START_TIME'] <= end_date);
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
    max1 = df.duration.quantile(0.95)
    if(math.isnan(max1)):
        return pd.DataFrame()
    else:
        query = 'duration > '+str(max1)
        tmp = pd.DataFrame(df.query(query), columns=['ID', 'START_TIME', 'CAUSE', 'duration']);
        return tmp;



def anomalyByDate(df, start_date, end_date):
    return anomaly(filter_date(df, start_date, end_date))



def mean(df):
    'period mean'
    return df.describe()['duration']['mean']


def study_frame( df, start, end, tab = []):
    #df         = create_dataframe(name, config2)
    periods    = []
    means      = []
    numAnormal = []
    num        = tab
    anormal    = []

    miny = int(start.split('-')[0])
    maxy = int(end.split('-')[0])
    minm = int(start.split('-')[1])
    maxm = int(end.split('-')[1])

    for year in range(miny,maxy+1):
        for i in range(minm, maxm+1):
            if(i == 12):
                start_date = str(year)+"-"+str(i)+"-01 00:00:00"
                end_date = str(year+1)+"-01-01 23:59:59"
            else:
                start_date = str(year)+"-"+str(i)+"-01 00:00:00"
                end_date = str(year)+"-"+str(i+1)+"-01 23:59:59"
            tmp = filter_date(df, start_date, end_date)
            if(math.isnan(mean(tmp)) == False):
                means.append(mean(tmp))
                periods.append(datetime.strptime(start_date, date_format))
                ano = anomalyByDate(tmp, start_date, end_date)
                anormal.append(ano)
                numAnormal.append(ano.index.size);
                #num.append( nJobs(config2['spooler'], start_date, end_date, config2))
    frame = pd.DataFrame()
    frame['period'] = pd.Series(periods)
    frame['mean']   = pd.Series(means)
    frame['num']    = pd.Series(num)
    frame['anormal'] = pd.Series(numAnormal)
    return frame



def df2jsonLine(df):
    n    = df.index.size
    arr1 = df.index;
    #arr2 = df.columns
    #m    = df.columns.size;
    arr2 = ['period', 'mean', 'anormal']
    m = 3

    json = '{"cols":[ {"id":"1", "label":"period", "type":"string"},{"id":"2", "label":"mean", "type":"number"},{"id":"3", "label":"anormal", "type":"number"} ] ,"rows":['
    for i in range(0, n):
        json += '{"c": ['
        for j in range(0, m):
            json += '{ "v" : "'+str(df[arr2[j]][arr1[i]])+'" }';
            if( j < m-1):
                json += ','
        json += ']}'
        if( i < n-1):
            json += ','
    json += ']}'
    return json




def df2jsonPie(df):
    v75  = df.duration.quantile(0.75)
    v95  = df.duration.quantile(0.95)
    vmax = v95 + (v95 - v75)

    mapPie = {
        'normal'    : df.query('duration <= '+str(v75)).index.size,
        'slow'      : df.query(str(v75)+'< duration <= '+str(v95)).index.size,
        'very slow' : df.query(str(v95)+'< duration <= '+str(vmax)).index.size,
        'too slow'  : df.query(str(vmax)+'< duration').index.size
    }

    json = '{"cols":'
    json +=  '[{"id": "type", "label": "Type", "type": "string"},'
    json +='{"id": "hours", "label": "Hours per Day", "type": "number"}],'
    json += '"rows":'
    json += '[{"c":[{"v": "Slow"}, {"v":'+ str(mapPie['slow'])+'}]},'
    json +='{"c":[{"v": "Too slow"},{"v":'+ str(mapPie['too slow'])+'}]},'
    json += '{"c":[{"v": "very slow"}, {"v":'+ str(mapPie['very slow'])+'}]},'
    json += '{"c":[{"v": "Normal"}, {"v":'+ str(mapPie['normal'])+'}]}]}'

    return json;



def df2jsonBox(df):
    n    = df.index.size
    arr1 = df.index;
    arr2 = ['START_TIME', 'ID', 'duration']
    m    = 3;
    json = "["
    for i in range(0, n):
        json += '{ "year"  : "'+str("2016")+'", "name" : "'+str(df[arr2[1]][arr1[i]])+'", "value" :'+str(df[arr2[2]][arr1[i]])+'}'
        if( i != n-1):
            json+= ','
    json +=']'
    return json
