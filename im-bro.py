#!/usr/bin/env python

from spacebro_client import SpacebroClient
from pathlib import Path
import json
import os
import sys, getopt
import collections
from PIL import Image

settings_files = ["settings/settings.default.json", "settings/settings.json"]
settings = {}
# get argv
def help():
    print 'qr-bro.py --settings <settingsfile>'
    print '-s <settingsfile>, --settings <settingsfile>'
    print '\t json settings file'

try:
  opts, args = getopt.getopt(sys.argv[1:],"hs:",["settings="])
except getopt.GetoptError:
  help()
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
     help()
     sys.exit()
  elif opt in ("-s", "--settings"):
     settings_files.append(arg)

def updateDeep(d, u):
	for k, v in u.iteritems():
		if isinstance(v, collections.Mapping):
			r = updateDeep(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = u[k]
	return d

# get settings
for file in settings_files:
  try:
    with open(file) as settings_file:
        updateDeep(settings, json.load(settings_file))
  except IOError:
    pass

# init folders
if not os.path.exists(settings['folder']['output']):
      os.makedirs(settings['folder']['output'])

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def make_image(input, output):
  im = Image.open(input)
  im = im.resize((850, 850), Image.BICUBIC)
  mark = Image.open(settings['media']['meta']['watermark']['path'])
  watermark(im, mark, (35, 35), 1).save(output)

def on_new_media(args):
  file_name = Path(args['path']).stem + '.png'
  file_path = os.path.join(settings['folder']['output'], file_name)
  make_image(args['path'], file_path)
  args.setdefault('details', {})
  args['details']['original'] = {'file': args['path'], 'type': args.get('type')}
  args['path']= file_path
  spacebro.emit(settings['service']['spacebro']['outputMessage'], args)
  print 'new image generated'
  print args


spacebro = SpacebroClient(settings['service']['spacebro']['host'], settings['service']['spacebro']['port'], {'clientName': settings['service']['spacebro']['clientName'], 'channelName': settings['service']['spacebro']['channelName'], 'verbose': False})

# Listen
spacebro.wait(seconds=1)
spacebro.on(settings['service']['spacebro']['inputMessage'], on_new_media)
spacebro.emit(settings['service']['spacebro']['inputMessage'], {'path': 'assets/image.png'})
spacebro.wait()
