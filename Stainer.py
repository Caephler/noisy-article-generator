import numpy
from PIL import Image
from pathlib import Path

class Stainer:
  def __init__(self):
    self.gen = StainGenerator()

  def stain(self, canvas, num_stains=1):
    for j in range(num_stains):
      self.gen.load_random_stain()
      opacity = (50 + numpy.random.randint(51)) / 100 
      canvas = self.gen.imprint(canvas=canvas, opacity=opacity)
    return canvas

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