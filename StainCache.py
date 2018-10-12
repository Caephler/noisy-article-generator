from PIL import Image
from pathlib import Path
import numpy

class StainCache:
  def __init__(self):
    self.cache = {}
    self.index_mapping = []
    self.get_stains()
    
  def get_stains(self):
    p = Path("./stains").glob("**/*.png")
    files = [str(x) for x in p if x.is_file()]
    for f in files:
      self.cache[f] = Image.open(f)
      self.index_mapping.append(f)

  def get_stain(self, src):
    if self.cache[src] != None:
      return self.cache[src]
    img = Image.open(src) 
    self.cache[src] = img
    return img
  
  def get_random_stain(self):
    choice = numpy.random.randint(len(self.index_mapping))
    f = self.index_mapping[choice]
    return self.get_stain(f)
