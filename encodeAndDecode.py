import numpy as np
import cv2

img = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [255, 255, 255], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

def encode(img):
    # pixel size to binary 16bit
    pixel_x_bit = '{0:016b}'.format(np.shape(img)[0])
    pixel_y_bit = '{0:016b}'.format(np.shape(img)[1])
    # pixel_x_bit = str(f'{np.shape(img)[0]:16b}')
    # pixel_y_bit = str(f'{np.shape(img)[1]:16b}')
    # print(pixel_x_bit)
    # print(pixel_y_bit)

    # encode the pixel size
    encode_bit = ""
    encode_bit += pixel_x_bit + pixel_y_bit

    # encode per pixel
    for i in range(np.shape(img)[0]):
        for j in range(np.shape(img)[1]):
            for rgb in range(3):
                encode_bit += str(f'{img[i][j][rgb]:08b}')
    # print(encode_bit)
    return encode_bit


def decode(encode_bits):
    # decode
    decode_img = []
    count_bit = 0

    # decode the pixel size
    pixel_x_int = int(encode_bits[0:16], 2)
    count_bit += 16
    # print(count_bit)
    pixel_y_int = int(encode_bits[16:32], 2)
    count_bit += 16
    # print(count_bit)
    # print(pixel_x_int)
    # print(pixel_y_int)
    # decode
    for i in range(pixel_x_int):
        decode_img.append([])
        for j in range(pixel_y_int):
            decode_img[i].append([])
            for rgb in range(3):
                decode_img[i][j].append(int(encode_bits[count_bit:count_bit + 8], 2))
                count_bit += 8
    # print(decode_img)
    np_decode_img = np.array(decode_img)
    return np_decode_img
encodebit = encode(img)
print(encodebit)
decode_img = decode(encodebit)
print(img)
print(decode_img)