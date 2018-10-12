from .ImageGenerator import CanvasGenerator 
from .ClipartImprinter import ClipartInserter
from .TextImprinter import FontEngine, TextImprinter
from .Artifacter import Artifacter
from .Stainer import Stainer
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
  orig_canvas_size = args.canvas
  canvas_size = (int(orig_canvas_size[0] * 1.2), int(orig_canvas_size[1] * 1.05))
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

    # To prevent cutting off when rotating later on
    x_offset = canvas.size[0] * (0.01 + (numpy.random.rand() * 0.04))

    y_offset = 0

    y_offset = txt_imp.imprint(
      canvas=canvas, 
      source=lorem.paragraph(), 
      max_height=numpy.random.randint(height / 5, height / 3), 
      offset=(x_offset, y_offset)
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
      max_height=numpy.random.randint(height / 5, height / 3),
      offset=(x_offset, y_offset)
    )

    clean_canvas = canvas.crop((0, 0, orig_canvas_size[0], orig_canvas_size[1]))
    p = PurePath("./out/clean").joinpath("{}.png".format(i))
    clean_canvas.save(str(p))

    # Staining starts

    num_stains = numpy.random.randint(stains_min, stains_max + 1)
    canvas = arti.blur(canvas)
    canvas = arti.rotate(canvas, max_degree=3.5)
    canvas = stainer.stain(canvas=canvas, num_stains=num_stains)
    bottom_canvas = gen.generate_canvas()
    bottom_canvas.paste(canvas, (0, 0), canvas)
    canvas = bottom_canvas
    canvas = arti.add_overlay(canvas)
    canvas = arti.add_texture(canvas)

    dirty_canvas = canvas.crop((0, 0, orig_canvas_size[0], orig_canvas_size[1]))
    p = PurePath("./out/dirty").joinpath("{}.png".format(i))
    dirty_canvas.save(str(p))

    bar.update(i)