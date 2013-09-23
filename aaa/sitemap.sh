#!/usr/local/bin/bash

cd /usr/www/envs/mk_mk_ua/bin/

#workon

#/usr/local/bin/bash /usr/www/envs/initialize --rcfile /usr/www/envs/mk_mk_ua/bin/activate \
#/usr/www/envs/mk_mk_ua/bin/python django-admin.py refresh_sitemap
#source /usr/www/envs/mk_mk_ua/bin/activate
/usr/local/bin/bash --rcfile /usr/www/envs/mk_mk_ua/bin/activate \
/usr/www/envs/mk_mk_ua/bin/python django-admin.py refresh_sitemap
