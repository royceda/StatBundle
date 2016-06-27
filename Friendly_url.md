# Job's name and spooler from its id

```
host/job_name/?id=21166385
host/job_spooler/?id=21166385
```

- id: job's id in the database 


# Job's description

```
host/describe?id=21166385&from=2016-06-20%2010:33&to=2016-06-28%2010:33
```


# Job's history

```
host/job_xml_history/?id=21166385
```

# Charts and the list unusual instance of the last consulted job

```
host/barchart
host/piechart
host/linechart
host/boxplot
host/anomaly
```

# Seek a job

```
host/job_xml?jobname=HPI/HPIP_00001_BACKUPDB&spooler=jstech&type=like
````
- jobname 
- spooler : spooler name where you make your search
- type: like or equal 

