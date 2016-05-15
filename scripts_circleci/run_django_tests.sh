#!/bin/bash

cd Web
mysql -u root -e "CREATE USER facefinder@localhost IDENTIFIED BY 'facefinder2045'"
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'facefinder'@'localhost'"
python manage.py test
