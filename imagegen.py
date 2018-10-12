from ImageGenerator import CanvasGenerator 
from ClipartImprinter import ClipartInserter
from TextImprinter import FontEngine, TextImprinter
from Artifacter import Artifacter
from Stainer import Stainer
import lorem
import numpy
from pathlib import PurePath, Path
import progressbar

def make_dirs():
  if not Path("./out").exists():
    Path("./out").mkdir()
  if not Path("./out/clean").exists():
    Path("./out/clean").mkdir()
  if not Path("./out/dirty").exists():
    Path("./out/dirty").mkdir()

def generate(args):
  make_dirs()

  num_images = args.num_images
  canvas_size = args.canvas
  clipart_size_min = args.clipart_min
  clipart_size_max = args.clipart_max
  font_size_min = args.font_min
  font_size_max = args.font_max
  stains_min = args.stains_min
  stains_max = args.stains_max

  bar = progressbar.ProgressBar(max_value=num_images)

  engine = FontEngine()
  txt_imp = TextImprinter(engine)
  gen = CanvasGenerator(canvas_size)
  stainer = Stainer()
  clipart = ClipartInserter()
  arti = Artifacter()

  bar.update(0)
  for i in range(num_images):
    engine.load_random_font()
    font_size = numpy.random.randint(font_size_min, font_size_max + 1)
    engine.set_font_size(font_size)
    canvas = gen.generate_canvas()
    height = canvas.size[1]

    y_offset = 0

    y_offset = txt_imp.imprint(
      canvas=canvas, 
      source=lorem.paragraph(), 
      max_height=numpy.random.randint(height / 3, height / 2), 
      offset=(0, y_offset)
    )

    image_size = numpy.random.randint(clipart_size_min, clipart_size_max + 1)

    y_offset = clipart.imprint_with_probability(
      canvas=canvas,
      size=(image_size, image_size),
      y_offset=y_offset,
      probability=0.5
    )

    y_offset = txt_imp.imprint(
      canvas=canvas,
      source=lorem.paragraph(),
      max_height=numpy.random.randint(50, 100),
      offset=(0, y_offset)
    )

    p = PurePath("./out/clean").joinpath("{}.png".format(i))
    canvas.save(str(p))

    # Staining starts

    num_stains = numpy.random.randint(stains_min, stains_max + 1)
    stainer.stain(canvas=canvas, num_stains=num_stains)
    canvas = arti.blur(canvas)
    canvas = arti.rotate(canvas, max_degree=3)
    canvas = arti.add_overlay(canvas)
    p = PurePath("./out/dirty").joinpath("{}.png".format(i))
    canvas.save(str(p))

    bar.update(i)