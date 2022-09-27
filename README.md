# Base64 Tools
Simple script that has some handy tools for Base64 encoding and decoding.

The main objective is to be able to encode text or images to Base64 (that has previously been copied to the clipboard or written down in the command line), or decode a Base64 string. In the case of the images, the resulting string will have a particular format: 

```
data:image/EXTENSION;base64,BASE64_STRING
```

The resulting string (Base64 or clear text) will be automatically copied to the clipboard to make the script more comfortable to use.

The usage is: 
```
b64.py [-h] [-d DECODE | -dc | -u URL | -p PATH | -ci | -ct]
```
Where the optional arguments are:
```
  -h, --help                  show this help message and exit
  -d TEXT, --decode TEXT      decode Base64 string
  -dc, --decode_clipboard     decode Base64 string from clipboard
  -u URL, --url URL           URL of the image
  -p PATH, --path PATH        local path of the image (stored in a certain folder)
  -ci, --clipboard_image      image from the clipboard
  -ct, --clipboard_text       text from the clipboard
```

It is highly recommended to include the script in the PATH of the system in order to be able to call it without having to navigate to the script's location.
