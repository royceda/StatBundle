<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;



class ChartController extends Controller
{
  public function boxplotAction()
  {
    return $this->render('StatBundle:tempChart:boxChart.html.twig');
  }

  public function piechartAction()
  {
    return $this->render('StatBundle:tempChart:pieChart.html.twig');
  }

  public function barchartAction()
  {
    return $this->render('StatBundle:tempChart:barChart.html.twig');
  }

  public function linechartAction()
  {
    return $this->render('StatBundle:tempChart:lineChart.html.twig');
  }
}
