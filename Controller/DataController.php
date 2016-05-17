<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;



class DataController extends Controller
{
  /* DATA */

  public function dataframeAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'text/xml');
    return $this->render('StatBundle:tempChart:dataframe.xml.twig',array(), $response );
  }


  public function describeAction(){
    $response = new Response();
    $response->headers->set('Content-Type', 'text/xml');
    return $this->render('StatBundle:tempChart:gridStat.xml.twig',array(), $response );
  }



  public function index2Action($name)
  {
      return $this->render('StatBundle:Default:index.html.twig', array('name' => $name));
  }

}
