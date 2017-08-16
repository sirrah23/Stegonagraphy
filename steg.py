#!/usr/bin/env python3
from PIL import Image
import sys

BITS_PER_BYTE = 8

def read_image(imagefile):
    img = Image.open(imagefile)
    img_bytes = img.tobytes()
    return img.mode, img.size, img_bytes

def get_lsb(byte):
    return byte & 1

def get_ith_window(i, window_length, data):
    return data[i * window_length : i * window_length + window_length]

def zero_lsb(bytestream):
    lowest_zero = int("0b11111110",2)
    return bytes(([b & lowest_zero for b in bytestream]))

def str_to_bytes(s):
    return s.encode()

def bytes_to_bits_gen(bytestream):
    first_bit_mask = int('0b10000000',2)
    for b in bytestream:
        for _ in range(BITS_PER_BYTE):
            yield (b & first_bit_mask) >> (BITS_PER_BYTE-1)
            b <<= 1

def byte_to_bitarray(i):
    return list(map(int, list("{:08b}".format(i))))

def hide_msg_in_img(img_bytes, msg_bytes):
    res_img_bytes = [0] * len(img_bytes)
    msg_bit_rcv = bytes_to_bits_gen(msg_bytes)
    i = 0
    # TODO: Refactor this
    while i < len(img_bytes):
        try:
            next_msg_bit = next(msg_bit_rcv)
        except StopIteration:
            break
        res_img_bytes[i] = img_bytes[i] + next_msg_bit
        i += 1
    res_img_bytes[i:] = img_bytes[i:]
    return bytes(res_img_bytes)

def write_image(img_mode, img_size, img_bytes, output):
    Image.frombytes(img_mode, img_size, img_bytes).save(output)

def hide(imagefile, message):
    img_mode, img_size, img_bytes = read_image(imagefile) 
    msg_bytes = str_to_bytes(message)
    if len(msg_bytes)*BITS_PER_BYTE > len(img_bytes):
        print("Your image is not big enough to hide the message.")
        sys.exit(1)
    zero_lsb_bytes = zero_lsb(img_bytes)
    res_img_bytes = hide_msg_in_img(zero_lsb_bytes, msg_bytes)
    write_image(img_mode, img_size, res_img_bytes, "./test.png")
    print(str(len(msg_bytes)) + " bytes written successfully to " + "./test.png")

def build_hidden_data(source_bytes, bytes_in_secret):
    res = ""
    for i in range(bytes_in_secret):
        curr_bytes = get_ith_window(i, BITS_PER_BYTE, source_bytes)
        res += chr(int(''.join(list(map(lambda b: str(get_lsb(b)), curr_bytes))),2))
    return res

def reveal(imagefile, bytes_in_secret):
    _, _, img_bytes = read_image(imagefile)
    res = build_hidden_data(img_bytes, bytes_in_secret)
    print(res)

action = sys.argv[1]
input_file = sys.argv[2]
input_param = sys.argv[3]
if action == "hide":
    hide(input_file, input_param)
elif action == "reveal":
    reveal(input_file, int(input_param))
else:
   print("Invalid operation " + action) 
   sys.exit(1)
sys.exit(0)
