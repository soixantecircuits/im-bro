im-bro is a tool to process images in the [spacebro](https://github.com/spacebro/spacebro) galaxy.
For now it is only watermarking.

## Install
```
sudo pip install pillow
sudo pip install pathlib
sudo pip install socketIO_client
```

## Run

```
python im-bro.py
```

## Settings

Settings from `settings/settings.default.json` are loaded by default.
You can also mention some settings from the commandline. 

```
python im-bro.py --settings path/to/setting.json
```

## media

im-bro waits for an event with data following the [standard media](https://github.com/soixantecircuits/standard/blob/master/media.json)

The minimum details would be:

```
{
    "path": "path to a file / url",
}
```

## output

The resulting image will be mentioned in the the `media.path` and the original one in `media.details`:
```
 { 
   path: '/tmp/im-bro/image.png',
   details:
      { original:
          { type: null,
            file: 'path/to/image.png' 
          }
      }
 }
```
