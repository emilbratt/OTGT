
* creating a new application is as simple as creating a new directory
inside the ./applications directory with the name of the directory
determing the name (query string) that you pass after the '/' in the hyperlink

* In Application.php you need to create a class named Home (is called) if you
omit the second query string after the application name

* For the second query string, youll create a Class with the name
you want
Note: uppercase class naming convention will be accessable with an all lowercase
query string

* Lastly, within the class you need a public available method called run()
as this is the method that is called as it is hard-coded
