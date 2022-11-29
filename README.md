# Base64 Tools
Simple script that has some handy tools for Base64 encoding and decoding.

The main objective is to be able to encode text or images to Base64 (that has previously been copied to the clipboard or written down in the command line), or decode a Base64 string. In the case of the images, the resulting string will have a particular format: 

```
data:image/EXTENSION;base64,BASE64_STRING
```

The resulting string (Base64 or clear text) will be automatically copied to the clipboard to make the script more comfortable to use.

The usage is: 
```
b64.py [-h] [-d DECODE | -dc | -e ENCODE | -eu ENCODE_URL | -ep ENCODE_PATH | -eci | -ect]
```
Where the optional arguments are:
```
  -h, --help                                  Show this help message and exit
  -d DECODE, --decode DECODE                  Decode Base64 string
  -dc, --decode_clipboard                     Decode Base64 string from clipboard
  -e ENCODE, --encode ENCODE                  Encode string from input
  -eu ENCODE_URL, --encode_url ENCODE_URL     Encode image from its URL
  -ep ENCODE_PATH, --encode_path ENCODE_PATH  Encode image from local path (stored in a certain folder)
  -eci, --encode_clipboard_image              Encode image from the clipboard
  -ect, --encode_clipboard_text               Encode text from the clipboard
```

It is highly recommended to include the script in the PATH of the system in order to be able to call it without having to navigate to the script's location.
