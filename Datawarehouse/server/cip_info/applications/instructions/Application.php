<?php

/**
 *
 * TODO:
 *  add: generate QR code for quick access on handhields -> generate_qrcode()
 *
 */

class Instructions {

  protected $page = 'Instrukser';
  protected $environment;
  protected $hyperlink;
  protected $template;
  protected $navigation;
  protected $fileobject;
  protected $category;
  protected $instruction;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/instructions/TemplateInstructions.php';
    require_once '../applications/instructions/NavigationInstructions.php';
    require_once '../applications/instructions/ObjectStorageInstructions.php';

    $this->environment = new Environment();
    $this->hyperlink = new HyperLink();
    $this->fileobject = new ObjectStorageInstructions;
    $this->navigation = new NavigationInstructions();
    $this->template = new TemplateInstructions();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Instructions {

  public function run () {
    if ( isset($_GET['instruction']) and (isset($_GET['category'])) ) {
      $this->instruction = $_GET['instruction'];
      $this->category = $_GET['category'];
      $this->show_instruction();
      $this->template->print($this->instruction);
      return;
    }
    if (isset($_GET['category'])) {
      $this->category = $_GET['category'];
      $this->list_instructions();
      $this->template->print($this->page);
      return;
    }

    $this->list_categories_sub_navbar();
    $this->hyperlink->link_redirect('instructions/administrate');
    $this->template->hyperlink_button('Amdinistrer', $this->hyperlink->url);
    $this->template->line_break();
    $this->template->print($this->page);
  }

  private function list_categories_sub_navbar () {
    $sub_nav_links = array();
    $this->fileobject->list_content();
    foreach ($this->fileobject->content_list as $category) {
      $this->hyperlink->link_redirect_query('instructions', 'category', $category);
      $sub_nav_links[$category] = $this->hyperlink->url;
    }
    $this->template->sub_navbar($sub_nav_links);
  }

  private function list_instructions () {
    $this->fileobject->change_path($this->category);
    $this->fileobject->list_content();
    if (!empty($this->fileobject->content_list)) {
      foreach ($this->fileobject->content_list as $instruction) {
        $query = 'category=' . $this->category . '&' . 'instruction=' . $instruction;
        // tmp remove file extension and swap underscore with whitespace for readablilty
        $instruction_name = $instruction;
        $instruction_name = explode('.pdf', $instruction_name)[0];
        $instruction_name = str_replace('_', ' ', $instruction_name);
        $this->hyperlink->link_redirect_multi_query('instructions', $query);
        $sub_nav_links[$instruction_name] = $this->hyperlink->url;
      }
      $this->template->sub_navbar($sub_nav_links);
    } else {
      $this->template->message('Fant ingen instrukser for ' . $this->category);
    }
    $this->hyperlink->link_redirect('instructions');
    $this->template->hyperlink_button('Tilbake', $this->hyperlink->url);
  }

  private function show_instruction () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $query = 'api/instructions/v0/view/' . $this->category . '/' . $this->instruction;
    $this->hyperlink->link_redirect($query);
    $this->url_api = 'http://'.$host.':'.$port.'/qrcode/single/';
    $this->data_send = [
      'barcodes' => [$this->hyperlink->url],
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $this->url_api);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data_send));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    if ( curl_errno($curl) ) {
      if ( $this->environment->developement('show_debug') ) {
        $this->template->message('Error on curl request: ' . curl_error($curl));
      }
      $this->template->message('Ingen kontakt med strekkode generator: ' . $this->url_api);
    }
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close ($curl);

    $this->template->embed_pdf($this->hyperlink->url);
    $this->template->hyperlink_button('Fullskjerm', $this->hyperlink->url);
    if ($http_status_code == 201) {
      $this->template->button_show_qr_code();
    }
    $this->template->button_fetch_api_delete_instruction($this->category, $this->instruction);
    $this->template->message('Hold nede ALT og trykk venstre piltast for å gå ut av fullskjerm');
    $this->template->image_show($body);
  }

}



class Administrate extends Instructions {

  public function run () {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $this->handle_form();
    }
    $this->fileobject->change_path('');
    $this->fileobject->list_directories();

    if ( empty($this->fileobject->content_list) ) {
      // do not show upload instructions form before we have at least one category
      $this->template->message('Fant ingen kategorier, legg til minst en kategori først');
      $this->template->form_add_instruction_category();
    } else {
      // all set, we can show all forms
      $this->template->title('Last opp Instruks (må være PDF-fil)');
      $this->template->form_upload_instruction($this->fileobject->content_list);

      $this->template->title('Legg til Kategori');
      $this->template->form_add_instruction_category();

      $this->template->title('Slett Kategori (ADVARSEL: sletter alle instrukser for valgt kategori)');
      $this->template->form_delete_instruction_category($this->fileobject->content_list);
    }
    $this->template->line_break();
    $this->hyperlink->link_redirect('instructions');
    $this->template->hyperlink_button('Tilbake', $this->hyperlink->url);
    $this->template->print($this->page);
  }

  private function handle_form () {
    if ( isset($_POST['input_field_instructions_add_category'])) {
      // this is enough to add the category directory
      $this->fileobject->change_path($_POST['input_field_instructions_add_category']);
      return;
    }
    if ( isset($_POST['input_field_instructions_delete_category'])) {
      // this is enough to delete the category directory
      $this->fileobject->delete_path($_POST['input_field_instructions_delete_category']);
      return;
    }
    $this->upload_instruction();
  }

  private function upload_instruction () {
    if ( !(isset($_POST['input_field_instructions_select_category'])) ) {
      return;
    }
    $_key = 'input_field_instructions_upload_file';
    if ( !(isset($_FILES[$_key])) ) {
      return;
    }

    if ($_FILES[$_key]['type'] !== 'application/pdf') {
      // a false positive happens if any letter in pdf extension is upper-case
      $ext = pathinfo($_FILES[$_key]['name'], PATHINFO_EXTENSION);
      if (strtolower($ext) !== 'pdf') {
        $this->template->message('Varsel: Instrukser må være i PDF format..');
        return;
      }
    }
    $this->category = $_POST['input_field_instructions_select_category'];
    $this->instruction = $_FILES[$_key]['name'];
    $this->fileobject->change_path($this->category);
    $this->fileobject->upload_file($_key);
    if ($this->fileobject->upload_error) {
      $this->template->message($this->fileobject->message_error);
      return;
    }
    // filename might have been altered, we grab the correctone from fileobject
    $filname = $this->fileobject->get_name_file();
    $querystring = "category=$this->category&instruction=$filname";
    $this->hyperlink->link_redirect_multi_query('instructions', $querystring);
    $this->template->hyperlink_button('Gå til instruks', $this->hyperlink->url);

  }

}
