#!/usr/bin/env bash
# Setup web server for deployment of web_static

# update and install nginx
apt update && apt install -y nginx

# create new directory data, web_static, shared, releases and test directory
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

echo "Hello world" > /data/web_static/releases/test/index.html

current_path=/data/web_static/current
# Delete symbolic link if it already exists and create a new one
if [ -e $current_path ]; then
    rm -r $current_path
fi
ln -s /data/web_static/releases/test/ $current_path

# Change owner and group of /data to ubuntu
chown -R ubuntu:ubuntu /data

# backup
default=/etc/nginx/sites-available/default
cp $default /etc/nginx/sites-available/default.bak

HOSTNAME=$(hostname)
# Configuration to server /data/web_static/current when /hbnb_static is requested
printf "%s" "
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                add_header X-Served-By \"$HOSTNAME\";
                try_files \$uri \$uri/ =404;
        }

        location /redirect_me {
                return 301 https://google.com;
        }

        error_page 404  /404.html;

        location /hbnb_static {
                alias /data/web_static/current;
        }
} " > $default

service nginx restart
