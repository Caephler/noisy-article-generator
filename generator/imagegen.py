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
  canvas_size = args.canvas
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

  def dirty(canvas, i, name=None):
    # Staining starts
    num_stains = numpy.random.randint(stains_min, stains_max + 1)
    canvas = arti.blur(canvas)
    # some lost corners
    canvas = stainer.stain(canvas=canvas, num_stains=num_stains)
    bottom_canvas = Image.new('RGBA', canvas.size, color=(255, 255, 255, 255))
    bottom_canvas.paste(canvas, (0, 0), canvas)
    canvas = bottom_canvas
    canvas = arti.add_overlay(canvas)
    canvas = arti.add_texture(canvas)
    dirty_canvas = canvas
    # dirty_canvas.show()
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
    font_size = font_size_min
    subtitle_font_size = int(font_size * 1)
    title_font_size = int(font_size * 1)
    small_font_size = int(font_size * 1)
    engine.set_font_size(font_size)
    canvas = gen.generate_canvas()
    height = canvas.size[1]

    # To prevent cutting off when rotating later on
    x_offset = canvas.size[0] * (0.01 + (numpy.random.rand() * 0.04))

    y_offset = int(0.02 * height + (height * (numpy.random.rand() * 0.08)))

    # print title
    engine.set_font_size(title_font_size)
    y_offset = txt_imp.imprint_line_center(
      canvas=canvas,
      source=lorem.sentence()[:50],
      y_offset=y_offset
    )

    # print subtitle
    engine.set_font_size(subtitle_font_size)
    y_offset = txt_imp.imprint_line_center(
      canvas=canvas,
      source = lorem.sentence()[:100],
      y_offset=y_offset
    )

    # add linebreak
    y_offset += font_size

    # print paragraph
    # print some text
    engine.set_font_size(font_size)
    y_offset = txt_imp.imprint(
      canvas=canvas,
      source=lorem.paragraph(),
      max_height=numpy.random.randint(height / 5, height / 3),
      offset=(x_offset, y_offset)
    )
    y_offset += font_size

    # center image with probability
    should_have_image = numpy.random.rand() > 0.3
    if should_have_image:
      image_size = int(canvas.size[0] * (0.1 + (numpy.random.rand() * 0.2)))
      y_offset = clipart.imprint_center(
        canvas=canvas,
        size=(image_size, image_size),
        y_offset=y_offset)
      # print caption
      engine.set_font_size(small_font_size)
      string = "Figure {num}. {descr}".format(num=numpy.random.randint(0, 10), descr=lorem.sentence())
      y_offset = txt_imp.imprint_line_center(
        canvas=canvas,
        source=string,
        y_offset=y_offset)
      y_offset += small_font_size

    while y_offset < canvas.size[1] * 0.95:
      # print paragraph
      # print some text
      engine.set_font_size(font_size)
      y_offset = txt_imp.imprint(
        canvas=canvas,
        source=lorem.paragraph() * 5,
        max_lines=numpy.random.randint(2, 5),
        offset=(x_offset, y_offset)
      )
      y_offset += font_size
      should_have_image = numpy.random.rand() > 0.7
      if should_have_image:
        image_size = int(canvas.size[0] * (0.1 + (numpy.random.rand() * 0.2)))
        y_offset = clipart.imprint_center(
          canvas=canvas,
          size=(image_size, image_size),
          y_offset=y_offset)
        # print caption
        engine.set_font_size(small_font_size)
        string = "Figure {num}. {descr}".format(num=numpy.random.randint(0, 10), descr=lorem.sentence())
        y_offset = txt_imp.imprint_line_center(
          canvas=canvas,
          source=string,
          y_offset=y_offset)
        y_offset += small_font_size

    clean_canvas = canvas
    p = PurePath("./out/clean").joinpath("{}.png".format(i))
    clean_canvas.save(str(p))

    dirty(canvas, i)

    bar.update(i)
