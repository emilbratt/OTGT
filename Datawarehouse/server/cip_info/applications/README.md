### quick over-view
* creating a new application is as simple as creating a new directory
inside the ./applications directory with the name of the directory
determing the name (query string) that you pass after the '/' in the hyperlink

* In Application.php you need to create a class named Home which is called by
default if you omit the second query string after the application name

* For the second query string, you will have to create a Class with the name
according to the second query string
Note: class with Upper case name convention and query string all lower case

* Lastly, within the class that is called, you need a public available method
called run() because this is the method that is called by hard-code

### example:
* This is hypothetical code inside applications/lemon/Application.php (we call this app for, you guessed it; lemon)
```
<?php
// creating a mother class (optionally) with core functions for the app
class Lemon {
  function __construct () {
    ...
    ...
  }
  protected function some_func () {
    ... // a protected function can be called by an inherited instance of this class
    ... // is NOT available through any url, but functionality can be served via this class
    ...
  }
}

// creating the home class that will be called if second query string is omitted
class Home extends Lemon {
  public function run () {
    ... // this is where the entrypoint is for home visiting mydomain/lemon
    ...
    ...

  }

}

class Juice extends Lemon {
  public function run () {
    ... // this is where the entrypoint is for juice when visiting mydomain/lemon/juice
    ...
    ...
  }

}

```
