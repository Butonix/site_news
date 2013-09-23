
from PIL import Image, ImageFont, ImageDraw
from random import choice, randint
import tempfile
import settings
import time
import os

class Captcha(object):

    def __init__(self, filename=None):
        self._check_store_dir()
        if filename:
            self.filename = filename
            self.text = self._read()            
        else:
            self._generate()

        if self.text is not None:
            self.font = ImageFont.truetype(os.path.join(settings.CAPTCHA_FONTS, 'arial.ttf'), 18)
            self.size = list(self.font.getsize(self.text))
            self.width = self.size[0] + 20
            self.height = self.size[1] + 8

    def _check_store_dir(self):
        if not os.path.isdir(settings.CAPTCHA_STORE):
            os.mkdir(settings.CAPTCHA_STORE, 755)
        self._check_expired()
        
    def _check_expired(self):
        for file in os.listdir(settings.CAPTCHA_STORE):
            file = os.path.join(settings.CAPTCHA_STORE, file)
            if os.stat(file)[9] + settings.CAPTCHA_LIVING < time.time():
                os.remove(file)
                                
    def _generate(self):
        digits = ['0','1','2','3','4','5','6','7','8','9','0']
        self.text = ''.join([choice(digits) for x in range(choice([4,5]))]).lower()
        fd, filename = tempfile.mkstemp('', '', settings.CAPTCHA_STORE)
        self.filename = os.path.basename(filename)
        os.write(fd, self.text)
        os.close(fd)

    def _read(self):
        try:
            path = os.path.join(settings.CAPTCHA_STORE, self.filename)
            return ''.join(file(path, 'r'))
        except:
            return None

    def draw(self, response):
        img = Image.new('RGB', (self.width, self.height), settings.CAPTCHA_BGCOLOR)
        drawing = ImageDraw.Draw(img)
        drawing.text((10, 4), self.text, font=self.font, fill=settings.CAPTCHA_FGCOLOR)
        drawing.rectangle((1,1, self.width-2, self.height-2), outline=settings.CAPTCHA_FGCOLOR)
        
        alpha = Image.new('L', img.size, 0xFFFFFF)
        drawing = ImageDraw.Draw(alpha)
		
        for i in range(randint(2,5)):
            x = randint(10, self.width-10)
            y = randint(10, self.height-10)
            
            drawing.line((x, 2, x, self.height-3), fill=randint(150,250))
            drawing.line((2, y, self.width-3, y), fill=randint(150,250))

        img.putalpha(alpha)
        img.save(response, format='PNG')
    
    
    