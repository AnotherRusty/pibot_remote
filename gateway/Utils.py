#!/usr/bin/env python

'''
    untilities for python 3.x compatible
'''


# input func alias to raw_input
input = raw_input

# convert bytes to integer
def bytes_to_int(c):
    if bytes == str:    # python2
        return ord(c)
    return int(c)   # python3

# convert int to bytes
def int_to_bytes(d):
    if bytes == str:    # python2
        return bytes(bytearray([d]))
    return bytes([d])   # python3
