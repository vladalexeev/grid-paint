'''
Created on 30.07.2013

@author: Vlad
'''

import graphics.color as clr

class SvgImageWriter:
    '''
        The class writes graphics commands to stream in SVG format.
        'writer' should implement method 'write' with a single string paramerter
    '''
    
    def __init__(self, writer):
        self.writer=writer
    
    def startImage(self, width, height):
        self.writer.write(
                '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}">'.format(
                width, height))
        self.writer.write('<desc>Created by Grid Painter http://grid-painter.appspot.com</desc>')

    def endImage(self):
        self.writer.write('</svg>')
        
    def rectangle(self, rect, fill):
        '''
            rect - array [left, top, right, bottom]
            fill - color in hex or tuple form
        '''
        if type(fill) is tuple:
            color=clr.rgb_to_hex(fill)
        else:
            color=fill
            
        self.writer.write(
            '<rect x="{0}" y="{1}" width="{2}" height="{3}" fill="{4}" stroke-width="0" />'.format(
                          rect[0], rect[1], rect[2]-rect[0]+1, rect[3]-rect[1]+1, color))
        
    def polygon(self, points, fill):
        '''
            points - array of tuples with coordinates x, y
        '''
        if type(fill) is tuple:
            color=clr.rgb_to_hex(fill)
        else:
            color=fill
            
        path_str='M'+str(points[0][0])+' '+str(points[0][1])
        for p in points[1:]:                
            path_str+='L'+str(p[0])+' '+str(p[1])
        
        path_str+="Z"
        
        self.writer.write(
            '<path d="{0}" fill="{1}" stroke-width="0" />'.format(path_str, color))