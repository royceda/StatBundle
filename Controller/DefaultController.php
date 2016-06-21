<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;


class DefaultController extends Controller
{
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



public function jobsAction(){
      $request = Request::createFromGlobals();
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

      return  $this->redirectToRoute('Stat_jobs_xml');
    }

    public function form_dateAction(){
      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      return $this->render('StatBundle:Default:form_date.xml.twig',array(), $response );
    }


    public function historyJobAction(){
      //job name
      $request = Request::createFromGlobals();
      $id = $request->query->get('id');
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


      $ordered = $request->get('chained');
      $stopped = $request->get('only_warning');

      $history = $this->container->get('arii_jid.history');
      $Jobs = $history->Jobs(0, 1, $stopped, false, $job, $spooler);

      //print_r($Jobs);

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
          $list .='<cell>'.$job['runs'][0]['dbid'].'</cell>';

          $list .='<cell>'.$job['spooler'].'</cell>';

          $list .='<cell>'.$job['name'].'</cell>';
          if (isset($job['runs'])) {
            $list .='<cell>'.$job['runs'][0]['start'].'</cell>';
            $list .='<cell>'.$job['runs'][0]['duration'].'</cell>';
          }

          $list .= '<cell>'." ".'</cell>';

          $list .='</row>';
      }


      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      $list .= "</rows>\n";
      $response->setContent( $list );
      return $response;
    }

}
