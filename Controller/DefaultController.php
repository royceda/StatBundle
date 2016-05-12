<?php

namespace Arii\StatBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
        return $this->render('StatBundle:Default:index.html.twig');
    }

    public function index2Action($name)
    {
        return $this->render('StatBundle:Default:index.html.twig', array('name' => $name));
    }

}
