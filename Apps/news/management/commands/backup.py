from django.core.management.base import BaseCommand
from datetime import datetime
import settings
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.now()
        
        # дамп базы
        
        dst = '%s/mk.mk.ua-%s.sql' % (settings.ROOT, now.strftime('%Y-%m-%d'))
        cmd = 'mysqldump %s --add-drop-database --user=%s --password=%s > %s' % (
            settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_PASSWORD, dst)            
        os.system(cmd)

        # дамп файлов сайта
        
        os.chdir(settings.ROOT)
        cmd = 'tar cfz ../mk.mk.ua-%s.tar.gz .' % (
            now.strftime('%Y-%m-%d'), )
            
        os.system(cmd)        
        os.unlink(dst)