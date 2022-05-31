<?php

 /**
  *
  * this script handles file uploads, read files and deletes them
  *
  */

class ObjectStorage {

  protected $path_root; // path as defined in environment.ini
  protected $path_current; // path that will be taken into account
  protected $path_file; // absolute path to file object
  protected $name_file; // filename (without path)
  protected $re_trailing_slash; // filename (without path)
  protected $re_no_hidden; // hidden files and folders
  public $content_list; // array of content of directory
  public $message_error; // on any error, message will appear here
  public $error; // on any operation error, set to true
  public $message_ok; // on any success, message MIGHT appear here

  function __construct () {
    $this->re_trailing_slash = '~^/.*/$~';
    $this->re_no_hidden = '/^([^.])/';
    $this->get_asset_root_path();
    $this->path_current = $this->path_root;
    $this->check_writable();
  }

  private function get_asset_root_path () {
    $environment = new Environment();
    $this->path_root = $environment->assets('webserver');
    // if no trailing forward slash, we add it
    if ( ! (preg_match($this->re_trailing_slash, $this->path_root)) ) {
      $this->path_root .= '/';
    }
  }

  private function remove_hidden () {
    // remove entries of the content list that starts with a dot
    $this->content_list = preg_grep ($this->re_no_hidden, $this->content_list);
  }

  protected function check_exist () {
    if ( is_dir($this->path_current) ) {
      return;
    }
    $dir_ok = mkdir($this->path_current, $permissions = 0777, $recursive = true);
    if ($dir_ok) {
      $this->message_ok = 'created ' . $this->path_current;
      return;
    }
    $user = exec('whoami');
    echo 'the path for assets (file uploads):<br>';
    echo '<strong>' . $this->path_current . '</strong><br>';
    echo 'could not be created<br>';
    echo '<br>';
    echo 'make sure ' . $this->path_current . ' exists and is writable by user:<br>';
    echo '<strong>' . $user . '</strong><br>';
    echo '<br>';
    echo 'script terminated';
    exit(1);
  }

  protected function check_writable () {
    if ( !(is_writable($this->path_current)) ) {
      $user =  exec('whoami');
      echo 'the path for assets (file uploads):<br>';
      echo '<strong>' . $this->path_current . '</strong><br>';
      echo 'is not writable<br>';
      echo '<br>';
      echo 'make sure it writable by user:<br>';
      echo '<strong>' . $user . '</strong><br>';
      echo '<br>';
      echo 'script terminated';
      exit(1);
    }
  }

  protected function set_root_path ($directory) {
    // should only be called once and in the beginning for a single instance
    // the instantiated object will only be ableto access contents inside here
    $this->path_root = $this->path_root . $directory . '/';
    if ( ! (preg_match($this->re_trailing_slash, $this->path_root)) ) {
      $this->path_root .= '/';
    }
    $this->path_current = $this->path_root;
    $this->check_exist();
    $this->check_writable();
  }

  public function set_path_file ($path_filename) {
    // pass the path that will be concatenated to $path_root for the absolute
    // path to the file that you want to handle or create etc.
    if ( ! (preg_match($this->re_trailing_slash, $this->path_root)) ) {
      $this->path_file .= '/';
    }
    $this->path_file = $this->path_root . $path_filename;
    $this->normalize_path_file();
    if ( !(is_file($this->path_file)) ) {
      $this->message_error = $this->path_file . ' does not exist or is not at file';
      return false;
    }
    return true;
  }

  protected function normalize_path_file () {
    // swap out whitespace with underscore etc.
    $this->path_file = str_replace(' ', '_', $this->path_file);
    $this->path_file = str_replace('!', '_', $this->path_file);
  }

  public function list_content () {
    // lists the content of path_current-> you can change this with change_path()
    $this->content_list = scandir($this->path_current);
    $this->remove_hidden();
  }

  public function list_directories () {
    // lists the directories of path_current-> you can change this with change_path()
    $tmp_content_list = scandir($this->path_current);
    $this->content_list = array();
    foreach ($tmp_content_list as $content) {
      if ( is_dir($this->path_current . $content) ) {
        array_push($this->content_list, $content);
      }
    }
    $this->remove_hidden();
  }

  public function change_path ($directory) {
    // changes the path to the path defined in the function parameter..
    // remember that it only changes the path within the path_root that
    // might have changed depending on if set_root_path() has been called
    $this->path_current = $this->path_root . $directory;
    $this->path_current = str_replace(' ', '_', $this->path_current);
    if ( ! (preg_match($this->re_trailing_slash, $this->path_current)) ) {
      $this->path_current .= '/';
    }
    $this->check_exist();
    $this->check_writable();
  }

  public function change_filename ($filename) {
    $this->name_file = $filename;
    $this->path_file = $this->path_current . $filename;
  }

  public function delete_path ($path = '') {
    // WARNING: this will recursively delete everything in that path
    if ( exec('rm -rf ' . $this->path_current . $path) ) {
      return true;
    }
    $this->message_error = 'something wrong when trying to delete ' . $this->path_current . $path;
    return false;
  }

  public function delete_file () {
    if ( !(isset($this->path_file)) ) {
      $this->message_error = 'no file path is set in "$path_file"';
      return false;
    }
    if ( !(is_file($this->path_file)) ) {
      $this->message_error = $this->path_file . ' does not exist or is not at file';
      return false;
    }
    if ( unlink($this->path_file) ) {
      return true;
    }
    $this->message_error = 'error on removing ' .  $this->path_file;
    return false;
  }

  public function read_file () {
    if ( !(isset($this->name_file)) ) {
      $this->message_error = 'no filename is set in "$name_file"';
    }
    $this->path_file = $this->path_current . $this->name_file;
    $this->normalize_path_file();
    readfile($this->path_file);
  }

  public function get_name_file () {
    return $this->name_file;
  }

  public function get_path_file () {
    return $this->path_file;
  }

}
