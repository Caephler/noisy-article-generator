from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import numpy
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

class TextImprinter:
  def __init__(self, font_engine):
    self.font_engine = font_engine

  def set_font_size(self, size=10):
    self.font_engine.set_font_size(size)
  
  def get_space_width(self):
    return self.font_engine.writing_font.getsize(" ")[0]
  
  def get_font_height(self):
    return self.font_engine.font_size
  
  def get_line_splits(self, canvas, source):
    font = self.font_engine.writing_font
    space_width = self.get_space_width()

    x_offset = 0
    result = []
    current_words = []
    words = source.split(" ")
    for word in words:
      width = font.getsize(word)[0]
      x_offset += width
      x_offset += space_width
      current_words.append(word)
      if x_offset > canvas.size[0]:
        x_offset = 0
        result.append(" ".join(current_words))
        current_words = []
    
    return result
  
  def imprint(self, canvas, source="", max_lines=3, offset=(0, 0)):
    cv = ImageDraw.Draw(canvas)
    splits = self.get_line_splits(canvas, source)[:max_lines]

    y_offset = offset[1]
    for line in splits:
      cv.text((0, y_offset), line, fill=(0, 0, 0), font=self.font_engine.writing_font)
      y_offset += self.get_font_height()

    return y_offset
    