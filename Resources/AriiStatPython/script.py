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


try:
    #print1();
    pd.DataFrame();
    name = str(sys.argv[1]);
    spooler = sys.argv[2];
    start = sys.argv[3];
    end = sys.argv[4];
    df = create_dataframe(name, spooler, config1);
    df = filter_date(df, start, end);
    xml = dfDescribe2xml(df.describe());
    writeXML('../views/tempChart/gridStat.xml.twig', xml);
    #print xml;

    #start_date = "2016-04-10"
    #end_date = "2016-05-10"
    tmp = anomalyByDate(df, start, end)
    #print tmp.columns
    xml = df2xml(tmp)
    writeXML('../views/tempChart/anoStat.xml.twig', xml);

except Exception, e:
    print e
