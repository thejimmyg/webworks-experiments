# WebWorks Experiments

Actually at the moment only Python 3.2 code for Blackberry Playbook Tablet OS 2.1 is here. You can run the examples by installing BGShell from the appstore and then using the QNX's `python3.2` binary to run the apps.

## License

[GNU AGPL3](http://www.gnu.org/licenses/agpl-3.0.html)

## Setup

The `upload.py` script assumes you are behind a HTTPS server with basic auth.

If you use Apache you can do this:

~~~
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2ensite default-ssl
~~~

Choose a strong password:

~~~
sudo mkdir /srv/passwd
sudo htpasswd -bc /srv/passwd/.htpasswd [user] [pass]
~~~


You will now need to edit the default Apache SSL configuration.

~~~
vim  /etc/apache2/sites-enabled/default-ssl
~~~

Insert just before `</VirtualHost>`:

~~~
        ProxyRequests Off
        <Proxy *>
                AuthUserFile /srv/passwd/.htpasswd
                AuthName EnterPassword
                AuthType Basic
                require valid-user

                Order Deny,allow
                Allow from all
        </Proxy>
        ProxyPass / http://localhost:8022/
        ProxyPassReverse / http://localhost:8022/
~~~

Restart apache2.

~~~
sudo service apache2 restart
~~~

## Authorization

Get the auth header by sniffing the HTTP headers using a tool like Firefox's LiceHTTPHeaders whilst you sign in and place them in the `AUTH` variable at the top of `upload.py`.
