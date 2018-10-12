from PIL import Image

class CanvasGenerator:
  # The canvas generator.
  def __init__(self, canvas_size=(200, 200)):
    self.canvas_size = canvas_size
    
  def generate_canvas(self):
    img = Image.new('RGBA', self.canvas_size, color=(255, 255, 255))

    return img
