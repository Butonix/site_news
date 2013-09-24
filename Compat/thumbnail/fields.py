import os

from django.db.models import ImageField
from django.core.files.base import ContentFile
from django.db.models import signals

from Compat.thumbnail.utils import rescale


class ThumbField(ImageField):

    def __init__(self, source, size, *args, **kwargs):
        kwargs['blank'] = True
        super(ThumbField, self).__init__(*args, **kwargs)
        self.source = source
        self.size = size
        
    def contribute_to_class(self, cls, name):
        self._field_name = name
        super(ThumbField, self).contribute_to_class(cls, name)
        signals.pre_save.connect(self.force_rethumb, sender=cls, weak=False)
        
    def generate_thumb_name(self, original):
        filename = os.path.split(original)[-1].split('.')
        if len(filename) > 1:
            filename[-2] = filename[-2] + '.' + self._field_name
        else:
            filename.append('.'+self._field_name)
        return '.'.join(filename)

    def force_rethumb(self, instance, *args, **kwargs):
        source = getattr(instance, self.source, None)
        try:
            old_instance = instance._default_manager.get(pk=instance.pk)
            old_source = getattr(old_instance, self.source)
        except:
            old_source = None        

        try:
            src_empty = source.path
        except ValueError, e:
            src_empty = None
        
        try:
            if old_source is not None:
                old_empty = old_source.path
            else:
                old_empty = None
        except ValueError, e:
            old_empty = None
        
        if src_empty is None:
            return
                
        if old_empty is None or getattr(source, 'path') != getattr(old_source, 'path'):
            thumb = getattr(instance, self._field_name, )
            import Image as pil
            import os
            try:
                img = pil.open(source.path, )
            except IOError:
#                pub_date = getattr(instance, 'pub_date', None, )
#                if pub_date:
#                    filename = source.name.split('/')[-1]
#                    source.name = 'photos/news/%s/%s' % (pub_date.strftime('%Y/%m/%d'), filename, )
                import os
                source.save(os.path.basename(source.path, ), source, save=False, )
                img = pil.open(source.path, )
                if old_source:
                    import os
                    os.system("rm " + old_source.path, )
            finally:
                filename = self.generate_thumb_name(source.path, )
                try:
                    raw = rescale(img, self.size[0], self.size[1])
                except UnboundLocalError:
                    import os
                    source.save(os.path.basename(source.path, ), source, save=False, )
                    img = pil.open(source.path, )
                    raw = rescale(img, self.size[0], self.size[1])
                thumb.save(name=filename, content=ContentFile(raw), save=False, )
                if old_source:
                    old_thumb = getattr(old_instance, self._field_name, )
                    import os
#                    old_thumb_path = old_thumb.path
                    os.system('rm ' + old_thumb.path, )
#                command = 'rm ' + 'photos/news/%s/' % add_date.strftime('%Y/%m/%d') + self.generate_thumb_name(old_source.path, )
#                raise Exception("Message")
