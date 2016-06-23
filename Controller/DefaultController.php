<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;

use Arii\CoreBundle\Service\AriiSession;

class DefaultController extends Controller{

  protected $ColorStatus = array (
  'SUCCESS' => '#ccebc5',
  'RUNNING' => '#ffffcc',
  'FAILURE' => '#fbb4ae',
  'STOPPED' => '#FF0000',
  'QUEUED' => '#AAA',
  'STOPPING' => '#ffffcc',
  'UNKNOW' => '#BBB'
);



/* CHART */
public function indexAction()
{
  return $this->render('StatBundle:Default:index.html.twig');
}



public function jobsAction(Request $request){
      //$request = Request::createFromGlobals();
      if ($request->get('history')>0) {
        $history_max = $request->get('history');
      }
      $stopped = $request->get('only_warning');

      $history = $this->container->get('arii_jid.history');
      $Jobs = $history->Jobs(0, 1, $stopped, false);

      $tools = $this->container->get('arii_core.tools');

      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      $list = '<?xml version="1.0" encoding="UTF-8"?>';
      $list .= "<rows>\n";
      $list .= '<head>
      <afterInit>
      <call command="clearAll"/>
      </afterInit>
      </head>';
      ksort($Jobs);

      //print_r($Jobs);

      foreach ($Jobs as $k=>$job) {
          if (isset($job['runs'])) {
              $status = $job['runs'][0]['status'];
          }
          else {
              $status = 'UNKNOW';
          }
          $list .='<row id="'.$job['runs'][0]['dbid'].'" style="background-color: '.$this->ColorStatus[$status].'">';
          $list .='<cell>'.$job['spooler'].'</cell>';

          $list .='<cell>'.$job['folder'].'/'.$job['name'].'</cell>';
          /*if (isset($job['runs'])) {
            $list .='<cell>'.$job['runs'][0]['start'].'</cell>';
          }*/
          $list .='</row>';
      }

      $list .= "</rows>\n";
      $response->setContent( $list );
      return $response;
    }




    public function datedJobsAction(Request $request, $date1, $date2){
      $request->getSession()->set('past', $date1 );
      $request->getSession()->set('future', $date2 );
    }




    public function form_dateAction(Request $request){
      $first = $request->query->get('first');

      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      return $this->render('StatBundle:Default:form_date.xml.twig',array(), $response );
    }


    public function historyJobAction(Request $request){
      //job name
      //$request = Request::createFromGlobals();
      $id = $request->query->get('id');

      $arr = $this->getInfos($id);
      $job = $arr['job'];
      $spooler = $arr['spooler'];


      $ordered = $request->get('chained');
      $stopped = $request->get('only_warning');

      $history = $this->container->get('arii_jid.history');
      $Jobs = $history->Jobs(0, 1, $stopped, false, $job, $spooler);

      //print_r($Jobs);
      $list = $this->productXML($Jobs, false);

      //$this->get('session')->set('currentJob', $job);
      //$this->get('session')->set('currentSpooler', $spooler);

      $request->getSession()->set('currentJob', $job);
      $request->getSession()->set('currentSpooler', $spooler );

      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      $response->setContent( $list );
      return $response;
    }


      public function jobAction(){
        //job name
        $request = Request::createFromGlobals();
        $jobname = $request->query->get('jobname');
        $spooler = $request->query->get('spooler');

        $type = $request->query->get('type');

        $from = $this->get('session')->get('past');
        $to = $this->get('session')->get('future');

        if($jobname != null ){
          if($type == "like"){
            $query = "select h.\"SPOOLER_ID\", h.\"JOB_NAME\"";
            $query .= " from SCHEDULER_HISTORY as h";
            $query .= " where h.\"JOB_NAME\" like '%".$jobname."%'";
            if($spooler != null){
              $query .= "and h.\"SPOOLER_ID\" like '%".$spooler."%'";
            }
            $query .= "and h.\"START_TIME\" between '".$from."' and '".$to."' limit 10";
            //echo $query;
          }else if($type == "equal"){
            $id = $request->query->get('id');
            $dhtmlx = $this->container->get('arii_core.dhtmlx');
            $sql = $this->container->get('arii_core.sql');
            $query = $sql->Select(array('h.SPOOLER_ID','h.JOB_NAME'))
                  .$sql->From(array('SCHEDULER_HISTORY h'));
            $query .= $sql->Where(array('h.ID'=>$jobname));
          }
          $only = true;
        }else{
          return $this->jobsAction($request);
        }

        $dhtmlx = $this->container->get('arii_core.dhtmlx');
        $data  = $dhtmlx->Connector('data');
        try{
          $res   = $data->sql->query( $query );
        }catch (Exception $e){
          echo $e->getMessage();
        }
        $Infos = $data->sql->get_next($res);

        $spooler =  $Infos['SPOOLER_ID'];
        $job     =  $Infos['JOB_NAME'];

        $history = $this->container->get('arii_jid.history');
        $ordered = $request->get('chained');
        $stopped = $request->get('only_warning');
        //echo $job;

        $Jobs = $history->Jobs(0, 1, $stopped, false, $job, $spooler);


        $list = $this->productXML($Jobs, $only);

        $response = new Response();
        $response->headers->set('Content-Type', 'text/xml');
        $response->setContent( $list );
        return $response;
      }



      private function productXML($Jobs, $only){
        //response
        $list = '<?xml version="1.0" encoding="UTF-8"?>';
        $list .= "<rows>\n";
        $list .= '<head>
        <afterInit>
        <call command="clearAll"/>
        </afterInit>
        </head>';

        ksort($Jobs);

        foreach ($Jobs as $k=>$job) {
          if (isset($job['runs'])) {
            $status = $job['runs'][0]['status'];
          }
          else {
            $status = 'UNKNOW';
          }
          $list .='<row id="'.$job['runs'][0]['dbid'].'" style="background-color: '.$this->ColorStatus[$status].'">';
          if($only == false){
            $list .='<cell>'.$job['runs'][0]['dbid'].'</cell>';
          }
          $list .='<cell>'.$job['spooler'].'</cell>';
          $list .='<cell>'.$job['name'].'</cell>';
          if (isset($job['runs'])) {
            $list .='<cell>'.$job['runs'][0]['start'].'</cell>';
            $list .='<cell>'.$job['runs'][0]['duration'].'</cell>';
          }

          $list .= '<cell>'." ".'</cell>';
          $list .='</row>';
        /*  if($only == true){
            break;
          }*/
        }
        $list .= "</rows>\n";
        return $list;
      }

      public function getNameAction(Request $request){
        $id = $request->query->get('id');

        $arr = $this->getInfos($id);
        $job = $arr['job'];
        $spooler = $arr['spooler'];

        $request->getSession()->set('currentJob', $job);
        $request->getSession()->set('currentSpooler', $spooler );

        $response = new Response();
        $response->headers->set('Content-Type', 'text');
        $response->setContent( $job );
        return $response;
      }

      public function getSpoolerAction(Request $request){
        $id = $request->query->get('id');

        $arr = $this->getInfos($id);
        $job = $arr['job'];
        $spooler = $arr['spooler'];

        $request->getSession()->set('currentJob', $job);
        $request->getSession()->set('currentSpooler', $spooler );

        $response = new Response();
        $response->headers->set('Content-Type', 'text');
        $response->setContent($spooler);
        return $response;
      }


      private function getInfos($id){
        //$id = $request->query->get('id');
        $dhtmlx = $this->container->get('arii_core.dhtmlx');
        $sql = $this->container->get('arii_core.sql');
        $qry = $sql->Select(array('h.SPOOLER_ID','h.JOB_NAME'))
              .$sql->From(array('SCHEDULER_HISTORY h'));
        $qry .= $sql->Where(array('h.ID'=>$id));

        $data = $dhtmlx->Connector('data');
        $res = $data->sql->query( $qry );
        $Infos = $data->sql->get_next($res);

        $spooler =  $Infos['SPOOLER_ID'];
        $job     =  $Infos['JOB_NAME'];

        return array("job" => $job, "spooler" => $spooler);
      }



  }
