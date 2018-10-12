from PIL import Image
from pathlib import Path
import numpy

class Texturer:
  def __init__(self):
    self.gen = TextureGenerator()

  def texture(self, canvas, probability=0.5):
    rand = numpy.random.random()
    if rand >= probability:
      return canvas
    self.gen.load_random_texture()
    canvas = self.gen.imprint(canvas=canvas)
    return canvas

class TextureGenerator:
  def __init__(self):
    self.cache = TextureCache()
    self.current_texture = None
  
  def load_random_texture(self):
    self.current_texture = self.cache.get_random_texture()
  
  def imprint(self, canvas):
    original_texture = self.current_texture.copy()
    size = original_texture.size
    start_x = int(numpy.random.rand() * (size[0] - canvas.size[0]))
    start_y = int(numpy.random.rand() * (size[1] - canvas.size[1]))
    coords = (start_x, start_y, start_x + canvas.size[0], start_y + canvas.size[1])
    texture = original_texture.crop(coords)
    final = Image.blend(canvas, texture.convert("RGBA"), 0.5)

    return final

class TextureCache:
  def __init__(self):
    self.cache = {}
    self.index_mapping = []
    self.get_textures()
    
  def get_textures(self):
    files = []
    p = Path("./textures").glob("**/*.png")
    files.extend([str(x) for x in p if x.is_file()])
    p = Path("./textures").glob("**/*.jpg")
    files.extend([str(x) for x in p if x.is_file()])
    for f in files:
      self.index_mapping.append(f)

  def get_texture(self, src):
    if self.cache.get(src) is not None:
      return self.cache.get(src)
    img = Image.open(src) 
    self.cache[src] = img
    return img
  
  def get_random_texture(self):
    choice = numpy.random.randint(len(self.index_mapping))
    f = self.index_mapping[choice]
    return self.get_texture(f)