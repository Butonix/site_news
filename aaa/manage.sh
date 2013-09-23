#!/bin/sh

mysqladmin --socket=/var/mysql.sock/mysql.sock drop mk_mk_ua
mysqladmin --socket=/var/mysql.sock/mysql.sock create mk_mk_ua
#python ./manage.py syncdb

#mysql --socket=/var/mysql.sock/mysql.sock mk_mk_ua