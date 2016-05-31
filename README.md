# StatBundle
----

StatBundle is a Symfony bundle to complete the project [Arii](https://github.com/AriiPortal/Arii) who use JobScheduller. The bundle enables to get statical vision about jobs such as: 
* Whiskers box
* Count, mean, standard deviation, min & max and some quantiles
* Chartplot of avery month with number of anormal instance and average time
* Pie of history which give the ratio of freak instance (about time)
* List of freak intance




# Getting started
----



## Librairies
---
 StatBundle uses python to compute especially with [Pandas librairy](www.github.com). So, you need to install the following packages which can be installed thanks to [pip](https://pypi.python.org/pypi/pip) or [easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall):
 * Numpy
 * Scipy
 * Matplotlib 
 * Datetime
 * psycopg2 (Cause PG database is used)
 * Pandas
 
Moreover, the Bundle use some functions of [AriiJIDBundle](https://github.com/AriiPortal/JIDBundle) and [AriiCoreBundle](https://github.com/AriiPortal/CoreBundle). 

## Installation
---


### Symfony project

In **app/AppKernel.php** 

```php
class AppKernel extends Kernel{
 public function registerBundles(){
  $bundles = array(
  /*....*/
  new Arii\StatBundle\StatBundle(),
  );
  /* .... */
 }
}
```

In **app/config/routing.yml**

````yml
stat:
    resource: "@StatBundle/Resources/config/routing.yml"
    prefix: /stat
````

### python config
In **config.py** adapt and paste the following code

```python
config = { 'dbname'   : '****',
           'user'     : '****',
           'host'     : '****',
           'password' : '****'
           }
```

NB: this manipulation is valid only for the first version. Afterward the python module will sync with JIDBundle DB configurations

### translation file in french

In **CoreBundle/Resources/translations/messages.fr.yml** add the following code

```yml
History : Historique
History in time : Historique dans le temps
Advanced : avancé
Histogram : Histogramme
Start date : Date de début
Duration : durée
count : compte
std : écart type
mean : moyenne
mean time : temps moyen
average : moyenne 
Value : Valeur
Scatter : Point
Box : Boîte
freaks : anomalies
Job states : états du job
Daily : Quotidien
Weekly : Hebdomadaire
Monthly : Mensuel
Visualization Type : Type de visualisation
```


# Using
---


![Screenshot](https://github.com/royceda/StatBundle/blob/master/Capture2.PNG?raw=true)
