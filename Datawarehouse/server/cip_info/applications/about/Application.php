<?php

class About {

  protected $page = 'Om'; // REMEMBER TO ADD THIS PAGE NAME SO THE CORRECT TOP MENU BAR IS HIGHLIGHET
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/about/TemplateAbout.php';
    require_once '../applications/about/NavigationAbout.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationAbout();
    $this->template = new TemplateAbout();

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends About {

  public function run () {
    $dev = $this->environment->contact_dev('name');
    $sysadm =$this->environment->contact_sysadmin('name');
    $staff = $this->environment->contact_staff('name');
    $dev_email = $this->environment->contact_dev('email');
    $sysadm_email =$this->environment->contact_sysadmin('email');
    $staff_email = $this->environment->contact_staff('email');
    $dev_phone = $this->environment->contact_dev('phone');
    $sysadm_phone =$this->environment->contact_sysadmin('phone');
    $staff_phone = $this->environment->contact_staff('phone');

    $m = <<<EOT
    <p>
    Denne siden brukes av ansatte hos C.I.Pedersen til å<br>
    finne informasjon om varer, lese instrukser, hente kontaktopplysninger<br>
    om ansatte og lese rapporter etc.<br>
    </p>
    EOT;
    $this->template->custom_html($m);

    $m = <<<EOT
    <p>
    Systemadministrator for datamaskiner og nettverk:
    <br><i>$sysadm<br>
    epost: $sysadm_email<br>
    telefon: $sysadm_phone</i><br><br>

    Ansvarlig for daglig drift:<br>
    <i>$staff<br>
    epost: $staff_email<br>
    telefon: $staff_phone</i><br><br>

    Lagerarbeider og utvikler:<br>
    <i>$dev<br>
    epost: $dev_email<br>
    telefon: $dev_phone</i><br><br>

    Siden er fremdeles under utvikling
    </p>
    EOT;
    $this->template->custom_html($m);
    $this->template->print();
  }

}
