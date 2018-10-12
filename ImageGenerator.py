from PIL import Image, ImageDraw, ImageFont
from pathlib import Path, PurePath
from StainCache import StainCache
import numpy
import lorem
import textwrap

class FontEngine:
  # The FontEngine
  def __init__(self):
    self.get_fonts()
    self.current_font_face = None
    self.writing_font = None
    self.font_size = 0

    pass
  
  def get_fonts(self):
    p = Path("./fonts").glob("**/*.ttf")
    files = [ str(x) for x in p if x.is_file()]

    self.fonts = files
  
  def load_random_font(self):
    choice = numpy.random.choice(self.fonts, 1)[0]
    self.current_font_face = choice
  
  def set_font_size(self, size=10):
    self.font_size = size
    self.writing_font = ImageFont.truetype(self.current_font_face, size=size)


class CanvasGenerator:
  # The canvas generator.
  def __init__(self):
    self.canvas_size = (0, 0)

  def set_params(self, canvas_size=(200, 200)):
    self.canvas_size = canvas_size
    
  def generate_canvas(self):
    img = Image.new('RGBA', self.canvas_size, color=(255, 255, 255))

    return img

class StainGenerator:
  def __init__(self):
    self.cache = StainCache()
    self.current_stain = None
  
  def load_random_stain(self):
    self.current_stain = self.cache.get_random_stain()

  def get_alpha_mask(self, image, opacity=1):
    paste_mask = image.convert("RGBA").split()[3].point(lambda i : i * opacity)
    
    return paste_mask

  
  def imprint(self, canvas, opacity=1):
    limit_x = canvas.size[0]
    limit_y = canvas.size[1]

    stain = self.current_stain.copy()
    stain_size = numpy.random.randint(numpy.floor(limit_x * 0.2), numpy.floor(limit_x * 0.8)) 
    stain.thumbnail((stain_size, stain_size))

    offset_x = -limit_x * 0.1 + numpy.random.randint(numpy.floor(limit_x))
    offset_y = -limit_y * 0.1 + numpy.random.randint(numpy.floor(limit_y))
    offset = (int(offset_x), int(offset_y))

    alpha_mask = self.get_alpha_mask(image=stain, opacity=opacity)

    final = Image.new("RGBA", canvas.size)
    final = Image.alpha_composite(final, canvas.convert("RGBA"))
    final.paste(stain, offset, alpha_mask)

    return final
