<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;





class DataController extends Controller
{
  /* DATA */

  public function dataframeAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'text/xml');
    return $this->render('StatBundle:tempChart:dataframe.xml.twig',array(), $response );
  }


  public function describeAction(){

    $request = Request::createFromGlobals();
    $id = $request->query->get('id');
    $from = $request->query->get('from');
    $to = $request->query->get('to');

    $dhtmlx = $this->container->get('arii_core.dhtmlx');
    $sql = $this->container->get('arii_core.sql');
    $qry = $sql->Select(array('h.SPOOLER_ID','h.JOB_NAME'))
          .$sql->From(array('SCHEDULER_HISTORY h'));
    $qry .= $sql->Where(array('h.ID'=>$id));

    $data = $dhtmlx->Connector('data');
    $res = $data->sql->query( $qry );
    $Infos = $data->sql->get_next($res);

    $spooler =  $Infos['SPOOLER_ID'];
    $name    =  $Infos['JOB_NAME'];

    //echo $spooler;
    //echo $name;

    //echo passthru('/usr/bin/python --version', $status);
    //$query1 = "ls /usr/local/lib/python2.7/dist-packages";
    //echo exec($query1, $output, $status);
    $query = 'cd /home/arii/Symfony/src/Arii/StatBundle/Resources/AriiStatPython/; ';
    $query .= "python script.py ".$name." ".$spooler." ".$from." ".$to;

    //echo $query;

    $output = system($query);
    //echo passthru($query1, $status);
    //echo $status;


    $response = new Response();
    $response->headers->set('Content-Type', 'text/xml');
    //$response->setContent($output);
    //return $response;
    return $this->render('StatBundle:tempChart:gridStat.xml.twig',array(), $response );
  }


  public function index2Action($name){
      return $this->render('StatBundle:Default:index.html.twig', array('name' => $name));
  }


  public function anomalyAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'text/xml');
    return $this->render('StatBundle:tempChart:anoStat.xml.twig',array(), $response );
  }


  public function piechartAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'application/json');
    return $this->render('StatBundle:tempChart:pieChart.json.twig');
  }


  public function barchartAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'application/json');
    return $this->render('StatBundle:tempChart:barChart.json.twig');
  }

  public function boxplotAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'application/json');
    return $this->render('StatBundle:tempChart:boxChart.json.twig');
  }


  public function linechartAction(){

    $request = Request::createFromGlobals();
    $period = $request->query->get('period');

    

    $response = new Response();
    $response->headers->set('Content-Type', 'application/json');
    return $this->render('StatBundle:tempChart:lineChart.json.twig');
  }

}
