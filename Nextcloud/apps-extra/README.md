## Installing self developed apps into Nextclouud server

### this guide is for nextcloud if installed to /var/www/html/nextcloud change if this is not the case

* enable the apps-extra path with keyword "apps_paths" by inserting into /var/www/html/nextcloud/config/config.php
<pre>
'apps_paths' =>
array (
  0 =>
  array (
    'path' => '/var/www/html/nextcloud/server/apps',
    'url' => '/apps',
    'writable' => true,
  ),
  1 =>
  array (
    'path' => '/var/www/html/nextcloud/server/apps-extra',
    'url' => '/apps-extra',
    'writable' => true,
  ),
),
</pre>

* cp -r this directory into /var/www/html/nextcloud/server/

* chown -R /var/www/html/nextcloud/server/apps-extra to http user (www-data for Debian/Ubuntu)

* Nextcloud should now be able to read the apps in this directory

* log on to nextcloud via webbrowser as admin and enable/disable apps via the app settings menu
