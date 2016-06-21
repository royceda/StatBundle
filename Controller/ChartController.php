<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;



class ChartController extends Controller
{
  public function boxplotAction()
  {
    return $this->render('StatBundle:Chart:boxChart.html.twig');
  }

  public function piechartAction()
  {
    return $this->render('StatBundle:Chart:pieChart.html.twig');
  }

  public function barchartAction()
  {
    return $this->render('StatBundle:Chart:barChart.html.twig');
  }

  public function linechartAction()
  {
    return $this->render('StatBundle:Chart:lineChart.html.twig');
  }
}
