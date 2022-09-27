import base64
import requests
import os
import pyperclip
from PIL import ImageGrab
import io
import argparse


# Function that parses the arguments
def parse():
    # Parser
    parser = argparse.ArgumentParser(description='Base64 Conversion')
    group = parser.add_mutually_exclusive_group()

    # Arguments and flags
    group.add_argument('-d', '--decode', required=False, action='store', help='Decode Base64 string')
    group.add_argument('-dc', '--decode_clipboard', required=False, action='store_true', help='Decode Base64 string from clipboard')
    group.add_argument('-u', '--url', required=False, action='store', help='URL of the image')
    group.add_argument('-p', '--path', required=False, action='store', help='Local path of the image (stored in a certain folder)')
    group.add_argument('-ci', '--clipboard_image', required=False, action='store_true', help='Image from the clipboard')
    group.add_argument('-ct', '--clipboard_text', required=False, action='store_true', help='Text from the clipboard')

    args = parser.parse_args()
    
    return args.decode, args.decode_clipboard, args.url, args.path, args.clipboard_image, args.clipboard_text


# Function that prints information with a certain header and length
def print_info(msg, title):
    # The lenght of the header depends on the lenght of the title
    header_len = (118 if len(title)%2 == 0 else 117)
    
    # The title will have the following format: #--- TITLE ---#
    header = f'#{"-"*int((header_len - len(title) - 2)/2)} {title} {"-"*int((header_len - len(title) - 2)/2)}#'

    # Print the header with message and the footer
    print(f'\n{header}')
    print(msg)
    print(f'#{"-"*header_len}#\n')


# Final step of the script: generate b64 string and copy it to the clipboard
def print_and_copy_result(b64_string, title, extension=None, decode=False):
    # First case: encode image, Second case: decode text, Third case: encode text
    b64 = (f'data:image/{extension};base64,{b64_string.decode("utf-8")}' if extension is not None else (b64_string if decode else b64_string.decode('utf-8')))
    
    pyperclip.copy(b64)
    print_info(b64, title)


# Image from URL
def image_url(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        b64_string = base64.b64encode(response.content)
        
        # Obtaining the extension of the file
        extension = url.split('/')[-1].split('.')[1]

        # Finish script
        print_and_copy_result(b64_string, 'Base64', extension)

    else:
        msg = f'Error while downloading the image from {url}'
        print_info(msg, 'Error')


# Image from URL
def image_path(path):
    # Path of the image to encode to Base64
    image = f'C://Users//adrian.manero//Pictures//Base64 Encoding//{path}'

    # Extension of the image to add to the final string
    name, extension = os.path.splitext(image)

    # Open image and encode to Base64
    with open(image, 'rb') as img:
        b64_string = base64.b64encode(img.read())

    # Finish script
    print_and_copy_result(b64_string, 'Base64', extension[1:])


# Image of text coming from clipboard
def clipboard(image=False):
    # Image
    if image:
        try:
            # Grab image from the clipboard and transform it into a stream of bytes in order to encode it into base64
            image = ImageGrab.grabclipboard()
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')

            b64_string = base64.b64encode(img_bytes.getvalue())

            # Finish script
            print_and_copy_result(b64_string, 'Base64', 'png')

        except AttributeError:
            msg = f'No image has been copied. The content of the clipboard is:\n{{{pyperclip.paste()}}}'
            print_info(msg, 'Error')

    # Text
    else:
        text = pyperclip.paste()
        text_bytes = text.encode('ascii')
        b64_string = base64.b64encode(text_bytes)
        print_and_copy_result(b64_string, 'Base64', None)


# Function to decode string from Base46
def decode_b64(decode, decode_cb):

    # Choosing the source of the b64 text: command line (first option) or clipboard (second option)
    b64 = (base64.b64decode(decode) if decode is not None else base64.b64decode(pyperclip.paste()))
    text = b64.decode('ascii')
    print_and_copy_result(text, 'Clear Text', decode=True)


def main():
    decode, decode_cb, url, path, cb_image, cb_text = parse()

    # DECODE BASE64 STRING
    if decode is not None or decode_cb: decode_b64(decode, decode_cb)

    # IMAGE FROM URL
    elif url is not None: image_url(url)

    # IMAGE FROM PATH
    elif path is not None: image_path(path)

    # IMAGE FROM CLIPBOARD
    elif cb_image: clipboard(image=True)

    # TEXT FROM CLIPBOARD
    elif cb_text: clipboard(image=False)

    # NO FLAG
    else: print_info('Please, specify a flag (use "b64 -h" o "b64 --help" to obtain help)', 'Error')


if __name__ == '__main__':
    main()
