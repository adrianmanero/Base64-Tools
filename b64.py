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
    group.add_argument('-e', '--encode', required=False, action='store', help='Encode string from input')
    group.add_argument('-eu', '--encode_url', required=False, action='store', help='Encode image from its URL')
    group.add_argument('-ep', '--encode_path', required=False, action='store', help='Encode image from local path (stored in a certain folder)')
    group.add_argument('-eci', '--encode_clipboard_image', required=False, action='store_true', help='Encode image from the clipboard')
    group.add_argument('-ect', '--encode_clipboard_text', required=False, action='store_true', help='Encode text from the clipboard')

    args = parser.parse_args()
    
    return args.decode, args.decode_clipboard, args.encode, args.encode_url, args.encode_path, args.encode_clipboard_image, args.encode_clipboard_text


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
    _, extension = os.path.splitext(image)

    # Open image and encode to Base64
    with open(image, 'rb') as img:
        b64_string = base64.b64encode(img.read())

    # Finish script
    print_and_copy_result(b64_string, 'Base64', extension[1:])


# Image of text coming from clipboard
def encode_from_clipboard(image=False):
    # Image
    if image:
        try:
            # Grab image from the clipboard and transform it into a stream of bytes in order to encode it into base64
            image = ImageGrab.grabclipboard()
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            encode_b64(img_bytes.getvalue(), 'png')
            # b64_string = base64.b64encode(img_bytes.getvalue())

            # # Finish script
            # print_and_copy_result(b64_string, 'Base64', 'png')

        except AttributeError:
            msg = f'No image has been copied. The content of the clipboard is:\n{{{pyperclip.paste()}}}'
            print_info(msg, 'Error')

    # Text
    else:
        encode_b64(pyperclip.paste().encode('ascii'))


# Function to encode a string to Base64
def encode_b64(text_bytes, extension=None):
    b64_string = base64.b64encode(text_bytes)
    print_and_copy_result(b64_string, 'Base64', extension)


# Function to decode string from Base64
def decode_b64(decode):
    b64 = ''
    # Choosing the source of the b64 text: command line (first option) or clipboard (second option)    
    if decode is not None:
        b64 = base64.b64decode(decode)

    else:
        # Checking if the string in the clipboard does not come from a b64 transformed image
        if pyperclip.paste().startswith('data'):
            raise Exception('The clipboard does not contain a regular b64 string, it is probably an image')
        else:
            b64 = base64.b64decode(pyperclip.paste())

    text = b64.decode('ascii')
    print_and_copy_result(text, 'Clear Text', decode=True)


def main():
    decode, decode_cb, encode, enc_url, enc_path, enc_cb_image, enc_cb_text = parse()

    # ENCODE FROM INPUT
    if encode is not None: encode_b64(encode.encode('ascii'))

    # DECODE BASE64 STRING
    elif decode is not None or decode_cb: decode_b64(decode)

    # ENCODE IMAGE FROM URL
    elif enc_url is not None: image_url(enc_url)

    # ENCODE IMAGE FROM PATH
    elif enc_path is not None: image_path(enc_path)

    # ENCODE IMAGE FROM CLIPBOARD
    elif enc_cb_image: encode_from_clipboard(image=True)

    # ENCODE TEXT FROM CLIPBOARD
    elif enc_cb_text: encode_from_clipboard(image=False)

    # NO FLAG
    else: print_info('Please, specify a flag (use "b64 -h" o "b64 --help" to obtain help)', 'Error')


if __name__ == '__main__':
    main()
