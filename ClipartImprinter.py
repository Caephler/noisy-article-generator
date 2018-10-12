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
