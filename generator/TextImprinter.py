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
    max_width = canvas.size[0] * 0.92

    x_offset = 0
    result = []
    current_words = []
    words = source.split(" ")
    for word in words:
      width = font.getsize(word)[0]
      if x_offset + width > max_width:
        x_offset = 0
        result.append(" ".join(current_words))
        current_words = []
      x_offset += width
      x_offset += space_width
      current_words.append(word)
    words.append(" ".join(current_words))

    return result

  def imprint_line_center(self, canvas, source="", y_offset=0):
    # enforce width < 80%
    cv = ImageDraw.Draw(canvas)
    max_width = canvas.size[0] * 0.8
    space_width = self.get_space_width()
    font = self.font_engine.writing_font

    total_width = 0
    words = []
    current_words = []
    widths = []
    for word in source.split(" "):
      width = font.getsize(word)[0]
      if total_width + width > max_width:
        widths.append(total_width)
        total_width = 0
        words.append(" ".join(current_words))
        current_words = []
      total_width += width + space_width
      current_words.append(word)
    words.append(" ".join(current_words))
    widths.append(total_width)

    for ind, line in enumerate(words):
      line_width = widths[ind]
      cv.text(((canvas.size[0] - line_width) / 2, y_offset), line, fill=(0, 0, 0), font=self.font_engine.writing_font)
      y_offset += self.get_font_height()

    return y_offset



  def imprint(self, canvas, source="", max_lines=3, max_height=None, offset=(0, 0)):
    cv = ImageDraw.Draw(canvas)
    y_offset = 0
    # max_height will take precedence, if max_height is set, we will use it instead
    # of max_lines
    if max_height != None:
      # using max_height
      splits = self.get_line_splits(canvas, source)
      x_offset = offset[0]
      y_offset = offset[1]
      for line in splits:
        cv.text((x_offset, y_offset), line, fill=(0, 0, 0), font=self.font_engine.writing_font)
        y_offset += self.get_font_height()
        if y_offset > max_height:
          break
    else:
      # using max_lines
      splits = self.get_line_splits(canvas, source)[:max_lines]

      x_offset = offset[0]
      y_offset = offset[1]
      for line in splits:
        cv.text((x_offset, y_offset), line, fill=(0, 0, 0), font=self.font_engine.writing_font)
        y_offset += self.get_font_height()

    return y_offset
