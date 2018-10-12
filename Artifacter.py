from PIL import ImageFilter, Image, ImageDraw, ImageOps
import numpy

class Artifacter:
  def __init__(self):
    self.predefined_overlays = [
      (0, 0, 0, 255),
      (242, 246, 208, 255),
      (143, 191, 224, 255),
      (255, 255, 255, 255)
    ]
    pass
  
  def blur(self, canvas, blur_radius=1):
    blur_radius = numpy.random.random() * blur_radius
    return canvas.filter(ImageFilter.GaussianBlur(blur_radius))

  def rotate(self, canvas, max_degree=4):
    sign = numpy.random.choice([-1, 1])
    degree = sign * numpy.random.random() * max_degree
    return canvas.rotate(degree)

  def add_overlay(self, canvas):
    color_index = numpy.random.randint(len(self.predefined_overlays))
    color = self.predefined_overlays[color_index]
    overlay = Image.new('RGBA', canvas.size, color)
    alpha = numpy.random.random() * 0.08
    return Image.blend(canvas, overlay, alpha)
