#!/bin/sh


echo "Hello Word" > /var/www/html/index.html
cp apache2.conf /etc/apache2/apache2.conf;
service apache2 restart;
cat /var/log/apache2/error.log
python tests/queue.py

