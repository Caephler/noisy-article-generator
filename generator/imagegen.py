from .ImageGenerator import CanvasGenerator
from .ClipartImprinter import ClipartInserter
from .TextImprinter import FontEngine, TextImprinter
from .Artifacter import Artifacter
from .Stainer import Stainer
import lorem
import numpy
from pathlib import PurePath, Path
import progressbar
from PIL import Image

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
  use_input = args.dirty_only


  engine = FontEngine()
  txt_imp = TextImprinter(engine)
  gen = CanvasGenerator(canvas_size)
  stainer = Stainer()
  clipart = ClipartInserter()
  arti = Artifacter()

  def dirty(canvas, i, name=None, crop=True):
    # Staining starts
    num_stains = numpy.random.randint(stains_min, stains_max + 1)
    canvas = arti.blur(canvas)
    # some lost corners
    orig_size = canvas.size
    expand_size = (int(canvas.size[0] * 1.12), int(canvas.size[1] * 1.12))
    canvas = canvas.resize(expand_size)
    canvas = arti.rotate(canvas, max_degree=3.5)
    canvas = canvas.crop((int(orig_size[0] * 0.06), int(orig_size[1] * 0.06), orig_size[0], orig_size[1]))
    canvas = stainer.stain(canvas=canvas, num_stains=num_stains)
    bottom_canvas = Image.new('RGBA', canvas.size, color=(255, 255, 255, 255))
    bottom_canvas.paste(canvas, (0, 0), canvas)
    canvas = bottom_canvas
    canvas = arti.add_overlay(canvas)
    canvas = arti.add_texture(canvas)
    dirty_canvas = canvas
    dirty_canvas.show()
    if crop and name is not None:
      dirty_canvas = canvas.crop((0, 0, orig_canvas_size[0], orig_canvas_size[1]))
    if name is None:
      p = PurePath("./out/dirty").joinpath("{}.png".format(i))
    else:
      p = PurePath("./out/dirty").joinpath("{}".format(name))
    dirty_canvas.save(str(p))

  if use_input:
    if not Path("./in").exists:
      print("directory does not exist")
    root_dir = Path("./in")
    walk = [f for f in root_dir.iterdir() if f.is_file()]
    images = []
    for f in walk:
      images.append((f.name, Image.open(f)))
    size = len(images)
    bar = progressbar.ProgressBar(max_value=size)
    bar.update(0)
    for index, image in enumerate(images):
      dirty(image[1], 0, name=image[0], crop=False)
      bar.update(index + 1)
    return

  bar = progressbar.ProgressBar(max_value=num_images)
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

    dirty(canvas)

    bar.update(i)
