<?php

require_once '../applications/Template.php';

class TemplateInstructions extends Template {

  function __construct () {
    parent::__construct();
  }

  public function _form_upload_instruction () {
    // this method is not done yet
    $this->html .= <<<'EOT'
    <form enctype="multipart/form-data" method="POST">
        <input type="hidden" name="MAX_FILE_SIZE" value="30000" />
        <!-- get notified within web browser if to large before starting upload -->

        <input name="input_field_upload" type="file" />
        <!-- this should put file path in: $_FILES['input_field_upload'] -->
        <input type="submit" value="Last opp" />
    </form>
    EOT;
    // should also check and verify the file came from browser with is_uploaded_file()
  }

}
