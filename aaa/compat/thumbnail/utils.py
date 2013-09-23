import Image as pil
from cStringIO import StringIO

def rescale(img, width, height, force=True):
    max_width = width
    max_height = height    
#    img = pil.open(data)
    format = img.format

    if not force:
        img.thumbnail((max_width, max_height), pil.ANTIALIAS)
    else:
        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(float(src_width - crop_width) / 2)
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(src_height - crop_height) / 3
        img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height), ))
        img = img.resize((dst_width, dst_height, ), pil.ANTIALIAS, )

    tmp = StringIO()
    img.save(tmp, format=format, quality=100)
    tmp.seek(0)
    output = tmp.getvalue()
    tmp.close()

    return output