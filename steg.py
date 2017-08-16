#!/usr/bin/env python3
from PIL import Image
import sys

def read_image(imagefile):
    img = Image.open(imagefile)
    img_bytes = img.tobytes()
    return img.mode, img.size, img_bytes

def zero_lsb(bytestream):
    lowest_zero = int("0b11111110",2)
    return bytes(([b & lowest_zero for b in bytestream]))

def str_to_bytes(s):
    return s.encode()

def bytes_to_bits_gen(bytestream):
    bits_per_byte = 8
    first_bit_mask = int('0b10000000',2)
    for b in bytestream:
        for _ in range(bits_per_byte):
            yield (b & first_bit_mask) >> (bits_per_byte-1)
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
            print(next_msg_bit)
        except StopIteration:
            break
        res_img_bytes[i] = img_bytes[i] + next_msg_bit
        i += 1
    res_img_bytes[i:] = img_bytes[i:]
    return bytes(res_img_bytes)

def write_image(img_mode, img_size, img_bytes, output):
    Image.frombytes(img_mode, img_size, img_bytes).save(output)

def hide(imagefile, message):
    # Get bytes from image along with mode/size
    img_mode, img_size, img_bytes = read_image(imagefile) 
    # Get bytes in the actual message
    msg_bytes = str_to_bytes(message)
    if len(msg_bytes)*8 > len(img_bytes):
        print("Your image is not big enough to hide the message.")
        sys.exit(1)
    # Zero out the lowest bit in each byte
    zero_lsb_bytes = zero_lsb(img_bytes)
    # Add lowest bit/msg to each byte of the image
    res_img_bytes = hide_msg_in_img(zero_lsb_bytes, msg_bytes)
    # Save out image with message inside
    write_image(img_mode, img_size, res_img_bytes, "./test.png")
    print(str(len(msg_bytes)) + " bytes written successfully to " + "./test.png")

input_file = sys.argv[1]
message = sys.argv[2]
hide(input_file, message)
sys.exit(0)
