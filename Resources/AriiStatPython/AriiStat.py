
import numpy as np;
import pandas as pd;
from datetime import datetime, date, timedelta
import psycopg2
import time
import math
import calendar

date_format = "%Y-%m-%d %H:%M:%S"


def create_dataframe(name, spooler, conf, lim=100000):
    #spooler = conf['spooler'];
    try:
        conn = psycopg2.connect("dbname='"+conf['dbname']+"' user='"+conf['user']+"' host='"+conf['host']+"' password='"+conf['password']+"'");
        if(name != None):
            df = pd.read_sql_query('select * from scheduler_history as sh where sh."JOB_NAME" = \''+name+'\' and sh."SPOOLER_ID" =\''+spooler+'\'  limit '+str(lim)+';',con=conn)
            #print df
            tab = []
            df = df.query("END_TIME != 'NaT'")
            #print df.index.size
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
    except Exception, e:
        print e
        print("I am unable to connect to the database: ");


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
    arr1 = ['duration'];
    arr = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows>";
    for i in range(0, len(arr1)):
        str1 += '<row id="'+str(arr1[i])+'">';
        str1 += '<cell>'+arr1[i]+'</cell>';
        for j in range(0, len(arr)):
            #str1 += '<cell>'+arr[j]+'</cell>';
            str1 += '<cell>'+str(float("{0:.2f}".format(df[arr1[i]][arr[j]])))+'</cell>';
        str1 += '</row>'
    str1 += '</rows>';
    return str1;


def df2xml(df, ano=False, df2=pd.DataFrame()):
    ''
    if(df2.empty == False):
        v75  = df2.duration.quantile(0.75)
        v95  = df2.duration.quantile(0.95)
        vmax = v95 + (v95 - v75)

    n    = df.index.size;
    m    = df.columns.size;
    arr1 = df.index;
    arr2 = df.columns;
    str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows>";
    for i in range(0, n):
        if(ano):
            if(df['duration'][arr1[i]] > vmax):
                str1 += '<row id="'+str(int(df[arr2[0]][arr1[i]]))+'" style="background-color: #fbb4ae">';
            else:
                str1 += '<row id="'+str(int(df[arr2[0]][arr1[i]]))+'" style="background-color: #ffffcc">';
        else:
            str1 += '<row id="'+str(int(df[arr2[0]][arr1[i]]))+'">';

        if(ano == True):
            str1 += '<cell>'+str(int(df[arr2[0]][arr1[i]]))+'</cell>';
        else:
            str1 += '<cell>'+str(df[arr2[0]][arr1[i]])+'</cell>';
        for j in range(1, m):
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
        str1 += '<row id="'+str(int(arr1[i]))+'">';
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


def study_frame( df, start, end, tab = [], period="month"):
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

    mind = min(int(start.split('-')[2]), int(end.split('-')[2]));
    maxd = max(int(start.split('-')[2]), int(end.split('-')[2]));

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



def df2jsonbar(df):
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




def df2jsonLine(df, pred=False):
    n    = df.index.size
    arr1 = df.index;
    #arr2 = df.columns
    #m    = df.columns.size;
    if(pred):
        arr2 = ['period', 'mean', 'pred']
        m = 3
    else:
        arr2 = ['period', 'mean']
        m = 2
    json = '{"cols":[ {"id":"1", "label":"period", "type":"string"},{"id":"2", "label":"mean", "type":"number"},{"id":"3", "label":"prediction", "type":"number"} ] ,"rows":['
    for i in range(0, n):
        json += '{"c": ['
        #{v: 'Date(2000, 8, 5)'} for 5/07/2000
        tmp_time = df[arr2[0]][arr1[i]]
        json += '{ "v" : "Date('+str(tmp_time.year)+','+str(tmp_time.month-1)+','+str(tmp_time.day)+')" },';
        for j in range(1, m):
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
    json += '[{"c":[{"v": "Too Slow"}, {"v":'+ str(mapPie['too slow'])+'}]},'
    json +='{"c":[{"v": "Very Slow"},{"v":'+ str(mapPie['very slow'])+'}]},'
    json += '{"c":[{"v": "Slow"}, {"v":'+ str(mapPie['slow'])+'}]},'
    json += '{"c":[{"v": "Normal"}, {"v":'+ str(mapPie['normal'])+'}]}]}'
    return json;



def df2jsonBox(df):
    n    = df.index.size
    arr1 = df.index;
    arr2 = ['START_TIME', 'ID', 'duration']
    m    = 3;
    json = "["
    for i in range(0, n):
        json += '{ "year"  : "'+str("0000")+'", "name" : "'+str(int(df[arr2[1]][arr1[i]]))+'", "value" :'+str(df[arr2[2]][arr1[i]])+'}'
        if( i != n-1):
            json+= ','
    json +=']'
    return json





def study_frame2(df, start, end,  period="month", tab = []):
    periods    = []
    means      = []
    numAnormal = []
    #num        = tab
    anormal    = []

    if(period  == "day"):
        d = start
        while (d <= end):
            delta = timedelta(days=1)
            e = d + delta
            tmp = filter_date(df, d, e)
            #print "from "+str(d)+" to "+str(e)
            #print tmp.index.size
            if(math.isnan(mean(tmp)) == False):
                means.append(mean(tmp))
                periods.append(d)
                ano = anomalyByDate(tmp, d, e)
                anormal.append(ano)
                numAnormal.append(ano.index.size);
            d = e;
    elif(period == "week"):
        d = start
        while d <= end:
            delta = timedelta(weeks=1)
            e = d + delta
            tmp = filter_date(df, d, e)
            #print "from "+str(d)+" to "+str(e)
            #print tmp.index.size
            if(math.isnan(mean(tmp)) == False):
                means.append(mean(tmp))
                periods.append(d)
                ano = anomalyByDate(tmp, d, e)
                anormal.append(ano)
                numAnormal.append(ano.index.size);
            d = e;
    elif(period == "month"):
        d = start
        while d <= end:
            year = d.year
            month = d.month
            maxi = calendar.monthrange(year, month)[1]
            delta = timedelta(days=maxi)
            e = d + delta
            tmp = filter_date(df, d, e)
            if(math.isnan(mean(tmp)) == False):
                means.append(mean(tmp))
                periods.append(d)
                ano = anomalyByDate(tmp, d, e)
                anormal.append(ano)
                numAnormal.append(ano.index.size);
            d = e;
    frame = pd.DataFrame()
    frame['period'] = pd.Series(periods)
    frame['mean']   = pd.Series(means)
    #frame['num']    = pd.Series(num)
    frame['anormal'] = pd.Series(numAnormal)
    return frame



def study_frame_pred(df, start, end,  period="month", tab = []):
    periods    = []
    means      = []
    numAnormal = []
    #num        = tab
    anormal    = []

    lock = True #to delete the firsts nan

    if(period  == "day"):
        d = start
        while (d <= end):
            delta = timedelta(days=1)
            e = d + delta
            tmp = filter_date(df, d, e)
            #print "from "+str(d)+" to "+str(e)
            #print tmp.index.size

            means.append(mean(tmp))
            periods.append(d)
            ano = anomalyByDate(tmp, d, e)
            anormal.append(ano)
            numAnormal.append(ano.index.size);
            d = e;

    elif(period == "week"):
        d = start
        while d <= end:
            delta = timedelta(weeks=1)
            e = d + delta
            tmp = filter_date(df, d, e)
            #print "from "+str(d)+" to "+str(e)
            #print tmp.index.size

            means.append(mean(tmp))
            periods.append(d)
            ano = anomalyByDate(tmp, d, e)
            anormal.append(ano)
            numAnormal.append(ano.index.size);
            d = e;

    elif(period == "month"):
        d = start
        while d <= end:
            year = d.year
            month = d.month
            maxi = calendar.monthrange(year, month)[1]
            delta = timedelta(days=maxi)
            e = d + delta
            tmp = filter_date(df, d, e)

            means.append(mean(tmp))
            periods.append(d)
            ano = anomalyByDate(tmp, d, e)
            anormal.append(ano)
            numAnormal.append(ano.index.size);
            d = e;

    frame = pd.DataFrame()
    frame['period'] = pd.Series(periods)
    frame['mean']   = pd.Series(means)
    #frame['num']    = pd.Series(num)
    frame['anormal'] = pd.Series(numAnormal)
    frame['pred'] = pd.Series(means).interpolate(method='pchip', limit_direction='both')
    #frame['pred'] = pd.Series(means).interpolate(method='spline', order=3, limit_direction='both')

    return frame
