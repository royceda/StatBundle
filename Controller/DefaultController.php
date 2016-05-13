<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;



class DefaultController extends Controller
{
  /* CHART */
    public function indexAction()
    {
        return $this->render('StatBundle:Default:index.html.twig');
    }


    public function boxplotAction()
    {
        return $this->render('StatBundle:tempChart:boxChart.html.twig');
    }


    public function piechartAction()
    {
        return $this->render('StatBundle:tempChart:pieChart.html.twig');
    }


    public function linechartAction()
    {
        return $this->render('StatBundle:tempChart:lineChart.html.twig');
    }

    /* DATA */

    public function jobsAction(){
      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      return $this->render('StatBundle:tempChart:jobs.xml.twig',array(), $response );
    }

    public function dataframeAction(){
      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      return $this->render('StatBundle:tempChart:dataframe.xml.twig',array(), $response );
    }


    public function describeAction(){
      $response = new Response();
      $response->headers->set('Content-Type', 'text/xml');
      return $this->render('StatBundle:tempChart:describe.xml.twig',array(), $response );
    }



    public function index2Action($name)
    {
        return $this->render('StatBundle:Default:index.html.twig', array('name' => $name));
    }

}
