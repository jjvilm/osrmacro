import cv2
import gtk
from PIL import Image as Image
import numpy as np
from cStringIO import StringIO
import autopy
import pyscreenshot as ImageGrab


def pyscrnsht():
    """Takes screenshot at given coordinates as PIL image format, the converts to cv2 grayscale image format"""
    im = ImageGrab.grab(bbox=(100,100,300,300)) #X1,Y1,X2,Y2
    im.show()
    print type(im)
    im=im.convert('RGB')
    print type(im)
    im = np.array(im)
    print type(im)

    cv_img = im.astype(np.uint8)
    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    print cv_img, cv_gray
    #template = cv2.imread("File/Of/Template.png", cv2.IMREAD_GRAYSCALE)

def screenshot(x=0, y=0, width=None, height=None):#Takes screenshot given then XY, coords, and Width and height
    window = gtk.gdk.get_default_root_window()
    if not (width and height):
        size - window.get_size()
        if not width:
            width = size[0]
        if not height:
            height = size[1]
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
    pixbuf = pixbuf.get_from_drawable(window, window.get_colormap(), x, y, 0, 0, width, height)
    
#    array = pixbuf.get_pixels_array()
    
    #return pixbuf2image(pixbuf), #converts to PIL image format
    return pixbuf

def pixbuf2image(pb):#converts from Pixbuf to PIL image format
    width,height = pb.get_width(),pb.get_height()
    return Image.frombytes("RGB",(width,height), pb.get_pixels() )

def stringio2opencv(img_stream, cv2_img_flag=0):#0 gray, 1, color, -1 Unchanged
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)


#pil_img = screenshot(500, 500, 100, 100)#takes screenshot saves to buff
pyscrnsht()
#autopy_img = autopy.bitmap.capture_screen(((500,500),(100,100)))
#x.save('welldone.png')#saves buffed image


