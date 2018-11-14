import argparse
from .imagegen import generate

def run():
  NUM_IMAGES = 10
  CANVAS_SIZE = (595, 842)
  FONT_SIZE_MIN = 16
  FONT_SIZE_MAX = 32
  STAINS_MIN = 0
  STAINS_MAX = 2

  parser = argparse.ArgumentParser(description="Generates images")
  parser.add_argument("-n", "--num-images", type=int, help="The number of images to generate. Defaults to {}.".format(NUM_IMAGES), default=NUM_IMAGES)
  parser.add_argument("-c", "--canvas", type=int, help="The dimensions of the square canvas. Defaults to {}x{}.".format(CANVAS_SIZE[0], CANVAS_SIZE[1]), nargs=2, default=CANVAS_SIZE)
  parser.add_argument("-d", "--dirty-only", help="You only want dirty images. Provide the input in in/*.png. Will ignore -n and -c.", action='store_true')
  parser.add_argument("--font-min", type=int, help="The minimum font size. Defaults to {}".format(FONT_SIZE_MIN), default=FONT_SIZE_MIN)
  parser.add_argument("--font-max", type=int, help="The maximum font size. Defaults to {}".format(FONT_SIZE_MAX), default=FONT_SIZE_MAX)
  parser.add_argument("--stains-min", type=int, help="The minimum number of stains on an image. Defaults to {}".format(STAINS_MIN), default=STAINS_MIN)
  parser.add_argument("--stains-max", type=int, help="The maximum number of stains on an image. Defaults to {}".format(STAINS_MAX), default=STAINS_MAX)

  args = parser.parse_args()
  generate(args)
