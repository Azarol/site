#!/usr/bin/env python

# ver 1.0

import sys
import os

if (len(sys.argv) < 2):
    print "Site name not found."
    sys.exit(0)

sitename = sys.argv[1]

vhost = """
<VirtualHost *:80>
	ServerAdmin ashibaev@demos.ru
	ServerName %s
	ServerAlias www.%s

	DirectoryIndex index.php index.html

	DocumentRoot /var/www/%s/www/

	LogLevel warn

	ErrorLog /var/www/%s/logs/error.log
	CustomLog /var/www/%s/logs/access.log combined
</VirtualHost>\n""" % ( sitename, sitename, sitename, sitename, sitename )

# create vhost config 
file = open( '/etc/apache2/sites-available/' + sitename, 'w' )
file.write( vhost )
file.close()

os.symlink( '/etc/apache2/sites-available/' + sitename, '/etc/apache2/sites-enabled/' + sitename );

# create site dirs
path = "/var/www/%s/" % sitename 
if not os.path.exists ( path ):
    os.makedirs ( path )

if not os.path.exists ( path + 'www/' ):
    os.makedirs ( path + 'www/' )

if not os.path.exists ( path + 'logs/' ):
    os.makedirs ( path + 'logs/' )

os.system( 'chown -R hooch:hooch ' + path )

# create local site name
file = open( '/etc/hosts', 'a' )
file.write( '127.0.0.1	' + sitename + "\n" )
file.close()

# reload apache config 
os.system( "apache2ctl graceful" )

print "All done.\n"
