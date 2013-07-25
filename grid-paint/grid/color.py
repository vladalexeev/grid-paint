# -*- coding: utf-8 -*-
'''
Created on 25 July 2013.

@author: Vlad
'''

def hex_to_rgb(value):
    value = value.lstrip('#')
    return tuple(float(int(value[i:i+2],16))/255 for i in [0, 2, 4])

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def darken_hls(hls, value):
    l=hls[1]-value
    if l<0:
        l=0
    return (hls[0],l,hls[2])

def lighten_hls(hls, value):
    l=hls[1]+value
    if l>1:
        l=1
    return (hls[0],l,hls[2])

def rgb256(r,g,b):
    return int(r*255),int(g*255), int(b*255)

if __name__ == "__main__":
    print str(hex_to_rgb('#ff0000'))