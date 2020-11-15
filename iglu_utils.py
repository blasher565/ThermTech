# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 14:58:12 2020

@author: Brandon Lasher

Contains some of the common operations to simply the code
"""


from PIL import Image, ImageTk


def resizeImage( filename, xSize, ySize ):
    global tmpImage
    tmpImage = Image.open(filename)
    tmpImage = tmpImage.resize((xSize,ySize), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image=tmpImage)

