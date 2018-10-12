from PIL import Image
from pathlib import Path
import numpy

class ClipartCache:
  def __init__(self):
    self.cache = {}
    self.index_mapping = []
    self.get_cliparts()
  
  def get_cliparts(self):
    p = Path("./clipart").glob("**/*.png")
    files = [str(x) for x in p if x.is_file()]
    for f in files:
      self.cache[f] = Image.open(f)
      self.index_mapping.append(f)

  def get_clipart(self, src):
    if self.cache[src] != None:
      return self.cache[src]
    img = Image.open(src)
    self.cache[src] = img
    return img
  
  def get_random_clipart(self):
    choice = numpy.random.randint(len(self.index_mapping))
    f = self.index_mapping[choice]
    return self.get_clipart(f)

class ClipartImprinter:
  def __init__(self):
    self.cache = ClipartCache()
    self.current_clipart = None

  def load_random_clipart(self):
    self.current_clipart = self.cache.get_random_clipart()
  
  def imprint(self, canvas, size=(64, 64), offset=(0, 0)):
    clipart = self.current_clipart.copy()
    clipart.thumbnail(size)
    canvas.paste(clipart, offset, clipart)

    return offset[1] + size[1]

  def imprint_left_align(self, canvas, size=(64, 64), y_offset=0, left_padding=0):
    return self.imprint(canvas, size, (left_padding, y_offset))

  def imprint_right_align(self, canvas, size=(64, 64), y_offset=0, right_padding=0):
    canvas_width = canvas.size[0]
    return self.imprint(canvas, size, (canvas_width - size[0] - right_padding, y_offset))

  def imprint_center_align(self, canvas, size=(64, 64), y_offset=0):
    canvas_width = canvas.size[0]
    return self.imprint(canvas, size, (int(canvas_width / 2 - size[0] / 2), y_offset))

class ClipartInserter:
  def __init__(self, padding=16):
    self.imprinter = ClipartImprinter()
    self.padding = padding
  
  def imprint_with_probability(self, canvas, size, y_offset, probability=0.5):
    n = numpy.random.random(1)[0]
    if n >= probability:
      self.imprinter.load_random_clipart()
      imprint_type = numpy.random.randint(3)
      if imprint_type == 0: # left align
        return self.imprinter.imprint_left_align(canvas, size, y_offset + self.padding, 16)
      elif imprint_type == 1: # center align
        return self.imprinter.imprint_center_align(canvas, size, y_offset + self.padding)
      elif imprint_type == 2:
        return self.imprinter.imprint_right_align(canvas, size, y_offset + self.padding, 16)
    return y_offset