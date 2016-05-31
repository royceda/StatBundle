try:
    import pip
    import sys
    import numpy
    import matplotlib
    import pandas as pd
    from AriiStat import *
except ImportError as e:
    print e
    #print "I/O error({0}): {1}".format(e.errno, e.strerror)



#Pour connaitre les librairies installe
def print1():
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
    for i in installed_packages])
    print(installed_packages_list)

def writeXML(file, xmlstr):
    try:
        f = open(file, 'w')
        f.write(xmlstr)
        f.close()
    except Exception, e:
        print e


def clearFiles():
    writeXML('../views/tempChart/lineChart_day.json.twig', "");
    writeXML('../views/tempChart/lineChart_week.json.twig', "");
    writeXML('../views/tempChart/lineChart_month.json.twig', "");

    writeXML('../views/tempChart/lineChart_day_pred.json.twig', "");
    writeXML('../views/tempChart/lineChart_week_pred.json.twig', "");
    writeXML('../views/tempChart/lineChart_month_pred.json.twig', "");

    writeXML('../views/tempChart/gridStat.xml.twig', "");
    writeXML('../views/tempChart/anoStat.xml.twig', "");
    writeXML('../views/tempChart/barChart.json.twig', "");
    writeXML('../views/tempChart/pieChart.json.twig', "");
    writeXML('../views/tempChart/boxChart.json.twig', "");


#In pred.py

def toto(df, start, end):

    try:
        m1 = calendar.monthrange(end.year, end.month)[1]
        #m2 = calendar.monthrange(end.year, end.month+1)[1]
        delta = timedelta(days = m1)
        end1 = end + delta

        tmp2 = study_frame_pred(df, start, end1, "month")
        json = df2jsonLine(tmp2, True)
        writeXML('../views/tempChart/lineChart_month_pred.json.twig', json);
    except Exception, e:
        err = "crash pred month"
        #print err

    try:
        delta = timedelta(weeks=2)
        end1 = end + delta

        tmp2 = study_frame_pred(df, start, end1, "week")
        json = df2jsonLine(tmp2, True)
        writeXML('../views/tempChart/lineChart_week_pred.json.twig', json);
    except Exception, e:
        err = "crash pred week"
        #print err

    try:
        delta = timedelta(days=2)
        end1 = end + delta
        tmp2 = study_frame_pred(df, start, end1, "day")
        json = df2jsonLine(tmp2, True)
        writeXML('../views/tempChart/lineChart_day_pred.json.twig', json);
    except Exception, e:
        err = "crash pred day"
        #print err


try:
    clearFiles()
    #print1();
    pd.DataFrame();
    name = str(sys.argv[1]);
    spooler = str(sys.argv[2]);
    start = str(sys.argv[3]) +" "+ str(sys.argv[4]);
    end = str(sys.argv[5]) +" "+ str(sys.argv[6]);

    #name = "ACV/check_open_event_0_AID_M001DWSCOACV"
    #spooler = "jsapp"
    #start = "2016-04-10"
    #end = "2016-05-10"

    #Description
    df = create_dataframe(name, spooler, config1);
    #print df;
    df = filter_date(df, start, end);
    xml = dfDescribe2xml(df.describe());
    writeXML('../views/tempChart/gridStat.xml.twig', xml);
    #print xml;

    #Anomalies potentielles
    tmp = anomalyByDate(df, start, end)
    xml = df2xml(tmp)
    writeXML('../views/tempChart/anoStat.xml.twig', xml);
    #print xml


    #barchart
    #start = "2015-01-01"
    #start = datetime(2015,1,1)
    tmp = start.split(" ")[0]
    start = datetime(int(tmp.split("-")[0]), int(tmp.split("-")[1]), int(tmp.split("-")[2]))
    tmp = end.split(" ")[0]
    end = datetime(int(tmp.split("-")[0]), int(tmp.split("-")[1]), int(tmp.split("-")[2]))
    tmp = study_frame2(df, start, end, "month")
    #print tmp
    json = df2jsonbar(tmp)
    writeXML('../views/tempChart/barChart.json.twig', json);
    #print json

    #PieCHart
    json = df2jsonPie(df)
    writeXML('../views/tempChart/pieChart.json.twig', json);

    #boxplot
    json = df2jsonBox(df)
    writeXML('../views/tempChart/boxChart.json.twig', json);
    #print json



    ######  Linechart
    tmp = study_frame2(df, start, end, "day")
    json = df2jsonLine(tmp);
    #print json
    writeXML('../views/tempChart/lineChart_day.json.twig', json);

    tmp = study_frame2(df, start, end, "week")
    json = df2jsonLine(tmp);
    #print json
    writeXML('../views/tempChart/lineChart_week.json.twig', json);

    tmp = study_frame2(df, start, end, "month")
    json = df2jsonLine(tmp);
    #print json
    writeXML('../views/tempChart/lineChart_month.json.twig', json);



    toto(df, start, end)
except Exception, e:
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rows><row><cell>ERROR</cell></row></rows>";
    writeXML('../views/tempChart/anoStat.xml.twig', xml);
    writeXML('../views/tempChart/gridStat.xml.twig', xml);
    print e
