import cv2 
import os
import numpy as np
import math
import sys

class LayerInfo:
    def __init__(self, dir, name, size, stride, offset):
        self.name = name
        self.size = size
        self.stride = stride
        self.offset = offset
        self.filename = "Compare_" + name.replace("<","_").replace(">","_") +".csv"
        self.reference = []
        self.compiled = []
        with open(os.path.join(dir, self.filename)) as csv:
           for line in csv:
               if not line.startswith("reference"):
                   values = line.rstrip().split(",")
                   self.reference.append(float(values[0]))
                   self.compiled.append(float(values[1]))
    
class LayerComparison:

    def __init__(self, reportFileName):
        self.layers = self.load(reportFileName)

    def load(self, filename):
      name = ""
      layers=[]
      dir = os.path.dirname(filename)
      with open(filename) as f:
        for line in f:
            if (line.startswith("## ")):
                name = line[3:].rstrip()
            if (line.startswith("size=")):
                i = line.index("[")
                j = line.index("]")
                size = line[i+1:j-1].split(",")
                size = list(map(int, size))
                                
                s = line.index("stride=")
                i = line.index("[", s)
                j = line.index("]", s)
                stride = line[i+1:j-1].split(",")
                stride = list(map(int, stride))
                
                s = line.index("offset=")
                i = line.index("[", s)
                j = line.index("]", s)
                offset = line[i+1:j-1].split(",")
                offset = list(map(int, offset))                
                
                print("loading layer ", name, " of size ", size, ", stride ", stride, ", offset", offset);
                layers.append(LayerInfo(dir, name, size, stride, offset))  
      return layers  
      
    def tileChannels(self, img, stride):
       w = stride[0]
       h = stride[1]
       channels = stride[2]
       rows = 1
       cols = 1
       while channels > 1:
           s = math.sqrt(channels)
           if (s == int(s)):
               cols = cols * int(s)
               rows = rows * int(s)
               channels = 1
           elif ((channels % 25) == 0):   
               cols = cols * 5
               rows = rows * 5
               channels = channels / 25
           elif ((channels % 10) == 0):   
               cols = cols * 5
               rows = rows * 2
               channels = channels / 10
           elif ((channels % 4) == 0):   
               cols = cols * 2
               rows = rows * 2
               channels = channels / 4
           else:
               cols = cols * int(channels)
               channels = 1
       c = 0
       result = np.zeros([h*rows,w*cols,1])
       for i in range(cols):
           for j in range(rows):
               x = i * w
               y = j * h
               result[y:y+h,x:x+w] = img[:,:,c:c+1]
               c = c + 1
       return result

    def compareImage(self, a, b):
        da = np.sum(a) 
        db = np.sum(b)
        result = da - db
        if (result < 0):
           result = -result
        result = result / da
        return result

    def compareTiles(self, a, b, ta, tb):
        stride = a.shape
        h = stride[0]
        w = stride[1]
        rows =int( ta.shape[0] / h)
        cols = int(ta.shape[1] / w)
        channels = stride[2]
        c = 0       
        for i in range(cols):
           for j in range(rows):               
               v = self.compareImage(a[:,:,c:c+1], b[:,:,c:c+1])
               if (v > 0.1):
                   print("comparing channel ", c, " found 10% difference ", v)
                   x = i * w
                   y = j * h
                   cv2.rectangle(ta, (x,y),(x+w,y+w),(0,0,255), 1)
                   cv2.rectangle(tb, (x,y),(x+w,y+w),(0,0,255), 1)
               c = c + 1

    def rgbImage(self, a):
        # scale array to range 0-1
        min = np.amin(a)
        max = np.amax(a)
        scale = 255.0 / (max - min);
        a = (a - min)
        if (min < max):
            a = a * scale;
        gray = a.astype(np.uint8)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR);
        
           
    def showLayer(self, i):
       layer = self.layers[i]
       print("Showing Layer " + layer.name + ", size=" + str(layer.size) + ", stride=" + str(layer.stride) + ", offset=" + str(layer.offset))
       stride = layer.stride
       name = "Reference Layer " + str(i) + ": " + layer.name
       a = np.reshape(layer.reference, stride)
       name2 = "Compiled Layer " + str(i) + ": " + layer.name
       b = np.reshape(layer.compiled, stride)

       ta = self.tileChannels(a, stride)
       tb = self.tileChannels(b, stride)

       ta = self.rgbImage(ta)
       tb = self.rgbImage(tb)

       self.compareTiles(a, b, ta, tb)
       
       cv2.imshow(name, ta)
       cv2.moveWindow(name, 0, 0)
       cv2.imshow(name2, tb)
       y = 0
       x = 0
       if (ta.shape[1] > 2 * ta.shape[0]):           
           y = ta.shape[0] 
           if (y < 150): y = 150   # this is the minimum window size
           y = y + 10
       else:
           x = ta.shape[1] 
           if (x < 316): x = 316   # this is the minimum window size
           x = x + 10
       cv2.moveWindow(name2, x, y)
       self.waitForEscape()
       cv2.destroyWindow(name)
       cv2.destroyWindow(name2)
       
    def waitForEscape(self):
        print("Press ESC to continue...")
        while True:
           if cv2.waitKey(1) & 0xFF == 27:
               break
       
    def showLayers(self):
       for i in range(len(self.layers)):
           self.showLayer(i)
               
if __name__ == '__main__':
  lc = LayerComparison(sys.argv[1])
  lc.showLayers()
  


   
   