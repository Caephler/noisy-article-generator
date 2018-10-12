from ImageGenerator import CanvasGenerator, StainGenerator
from ClipartImprinter import ClipartImprinter
from TextImprinter import FontEngine, TextImprinter
import lorem
import numpy
from pathlib import PurePath

NUM_IMAGES = 10

engine = FontEngine()
txt_imp = TextImprinter(engine)
gen = CanvasGenerator()
gen.set_params(canvas_size=(200, 200))
stain = StainGenerator()
clipart = ClipartImprinter()

for i in range(NUM_IMAGES):
  engine.load_random_font()
  font_size = numpy.random.randint(10, 40)
  engine.set_font_size(font_size)
  canvas = gen.generate_canvas()

  y_offset = txt_imp.imprint(canvas=canvas, source=lorem.paragraph(), max_lines=3, offset=(0, 0))

  image_padding = 16
  clipart.load_random_clipart()
  y_offset = clipart.imprint(canvas, 
    offset=(int(canvas.size[0] / 2) - 32, y_offset + image_padding),
    size=(64, 64)
  )
  # y_offset += image_padding

  y_offset = txt_imp.imprint(
    canvas=canvas,
    source=lorem.paragraph(),
    max_lines=3,
    offset=(0, y_offset)
  )

  p = PurePath("./out").joinpath("clean_{}.png".format(i))
  canvas.save(str(p))

  # Staining starts

  num_stains = numpy.random.randint(1, 3) # 1 to 2 stains
  for j in range(num_stains):
    stain.load_random_stain()
    # Set opacity to 0.50 to 1.00
    opacity = (50 + numpy.random.randint(51)) / 100 
    canvas = stain.imprint(canvas=canvas, opacity=opacity)
  p = PurePath("./out").joinpath("dirty_{}.png".format(i))
  canvas.save(str(p))
