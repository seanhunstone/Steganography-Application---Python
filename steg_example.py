import wx
import os
from scipy import misc
import PIL
from PIL import Image
from stegano import *

from shutil import copyfile
from stegano import exifHeader
from stegano import red
from stegano import lsbset
from stegano.lsbset import generators
#from .parity import *
#from .statistics import *

import operator
from PIL import Image
from collections import Counter
from collections import OrderedDict

class StegInterface(wx.Frame):    

    def __init__(self, *args, **kwargs):
        super(StegInterface, self).__init__(*args, **kwargs)

        

        self.initUI()
    
       
    def initUI(self):
        self.panel1=wx.Panel(self)
        wx.Panel.SetSize(self,780,480)
          

        #self.picture = wx.StaticBitmap(self.panel1, size=(200,300),pos=(100,100))
        #self.picture.SetBitmap(wx.Bitmap('Lena.jpg'))

        self.image = wx.Image("placeholder.jpg", wx.BITMAP_TYPE_ANY)
        self.picture = wx.StaticBitmap(self.panel1, -1, wx.Bitmap(self.image))
        
        self.plainText = wx.TextCtrl(self.panel1, wx.ID_ANY, pos=(50, 100), size=(300,100), style= wx.TE_MULTILINE)
        self.DecodeplainText = wx.TextCtrl(self.panel1, wx.ID_ANY, pos=(50, 260), size=(300,100), style= wx.TE_MULTILINE)
        self.encodeBtn = wx.Button(self.panel1, wx.ID_ANY, "Encode", pos=(260, 210))
        self.decodeBtn = wx.Button(self.panel1, wx.ID_ANY, "Decode", pos=(260, 370))
        self.openFileBtn = wx.Button(self.panel1, wx.ID_ANY, "Open a File", pos=(530, 400))
        self.resultLbl = wx.StaticText(self.panel1, wx.ID_ANY, "results will go here", pos=(50, 200))
        self.methodLbl = wx.StaticText(self.panel1, wx.ID_ANY, "Method", pos=(50, 40))
        self.DecodeLbl = wx.StaticText(self.panel1, wx.ID_ANY, "Decode an Image", pos=(50, 240))
        self.EecodeLbl = wx.StaticText(self.panel1, wx.ID_ANY, "Encode an Image", pos=(50, 80))
        self.ImagePathLbl = wx.StaticText(self.panel1, wx.ID_ANY, "", pos=(425, 35))
        
        self.Bind(wx.EVT_BUTTON, self.onEncodeBtn, id=self.encodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.onDecodeBtn, id=self.decodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.onOpenFileBtn, id=self.openFileBtn.GetId())

        #myList=['beef', 'tuna', 'cocnuts', 'more beef', 'cereal']
        #con = wx.ListBox(self.panel1, -1, (20,20), (80,30), myList, wx.LB_SINGLE)
        #con.SetSelection(0)

        self.choice = wx.Choice(self.panel1, pos=(100,35), choices=["HeaderFile", "LSB", "RedPortionPixel", "Eratosthenes", "Steganalyse" ])
        self.choice.Bind(wx.EVT_CHOICE, self.onChoice)
        
        
        
        

        self.Show(True)

  
    
        
    def onQuit(self, e):
        self.Close()

    def onEncodeBtn(self, evt):
        plainText = self.plainText.GetValue()

        self.origImage = misc.imread(self.imagePath)
        self.origImage = PIL.Image.fromarray(self.origImage)

        print("ORIGINAL:")
        print(steganalysis.steganalyse(self.origImage))

        steganalysis.parity.steganalyse(self.origImage).show()
        
        self.stegImage = lsb.hide(self.imagePath, plainText)
        #secret.save("lena_steg.png")
        self.stegImage.save("secret.png")

        #self.origImage = misc.imread("lena_steg.png")
        #self.origImage = PIL.Image.fromarray(self.origImage)

        #self.stegImage = misc.imread(self.imagePath)
        #self.stegImage = PIL.Image.fromarray(self.stegImage)
        
        #print("ORIGINAL:")
        #print(steganalysis.steganalyse(self.origImage))
        print("STEG:")
        print(steganalysis.steganalyse(self.stegImage))
        
        #steganalysis.parity.steganalyse(self.origImage).show()
        steganalysis.parity.steganalyse(self.stegImage).show()
        
        
        self.resultLbl.SetLabel("Message successfully encoded.")


    def onDecodeBtn(self, evt):
        
        clear_message = lsb.reveal("lena_steg.png")
        self.resultLbl.SetLabel(clear_message)
        

    def EncodeExifHeader(self, evt):
        plainText = self.plainText.GetValue()
        #string= StringVar.get()
        #string = plainText.get().split('/')[-1]
        messages_to_hide=[plainText]
        for message in messages_to_hide:
            secret = exifHeader.hide(self.imagePath, self.imagePath, secret_message=message)
        
            #self.assertEqual(message, message)
            #secret.save(self.imagePath)
            self.resultLbl.SetLabel("Message successfully encoded.")
            self.resultLbl.SetForegroundColour('green')
            

    def DecodeExifHeader(self, evt):
        print(self.imagePath)
        clear_message = exifHeader.reveal(self.imagePath)
        
        self.resultLbl.SetLabel(clear_message)
        self.DecodeplainText.SetValue(clear_message)

    def EncodeRedPortion(self, evt):
        plainText = self.plainText.GetValue()
        messages_to_hide=[plainText]
        for message in messages_to_hide:
            secret= red.hide(self.imagePath, plainText)
            secret.save(self.imagePath)
            self.resultLbl.SetLabel("Message successfully encoded.")

    def DecodeRedPortion(self, evt):
        clear_message = red.reveal(self.imagePath)
        self.resultLbl.SetLabel(clear_message)

    def EncodeEratosthenes(self, evt):
        plainText = self.plainText.GetValue()
        messages_to_hide=[plainText]
        for message in messages_to_hide:
            secret = lsbset.hide(self.imagePath, message, generators.eratosthenes())
            print(generators.eratosthenes())
            secret.save(self.imagePath)
            self.resultLbl.SetLabel("Message successfully encoded.")

    def steganalyse(self, img):
        img = self.imagePath
        encoded = img.copy()
        width, height = self.size
        colours_counter = Counter() # type: Counter[int]

        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                colours_counter[r] += 1

        most_common = colours_counter.most_common(10)
        dict_colours = OrderedDict(sorted(list(colours_counter.items()),
                                   key=lambda t: t[1]))

        colours = 0 # type: float
        for colour in list(dict_colours.keys()):
            colours += colour
        colours = colours / len(dict_colours)

        #return colours.most_common(10)
        return list(dict_colours.keys())[:30], most_common


    def hide(self, img, message):
        """
        Hide a message (string) in an image with the
        LSB (Least Significant Bit) technique.
        """
        encoded = img.copy()
        width, height = img.size
        index = 0
     
        message = message + '~~~'
        message_bits = "".join(tools.a2bits_list(message))
     
        npixels = width * height
        if len(message_bits) > npixels * 3:
            return """Too long message (%s > %s).""" % (len(message_bits), npixels * 3)
     
        for row in range(height):
            for col in range(width):
     
                if index + 3 <= len(message_bits) :
     
                    # Get the colour component.
                    (r, g, b) = img.getpixel((col, row))
     
                    # Change the Least Significant Bit of each colour component.
                    r = tools.setlsb(r, message_bits[index])
                    g = tools.setlsb(g, message_bits[index+1])
                    b = tools.setlsb(b, message_bits[index+2])
     
                    # Save the new pixel
                    encoded.putpixel((col, row), (r, g , b))
     
                index += 3
     
        return encoded
        self.resultLbl.SetLabel("Message successfully encoded.")


    def doMe(self, evt):
        #self.Destroy()
        plainText = self.plainText.GetValue()
        self.origImage = misc.imread(self.imagePath)
        self.origImage = PIL.Image.fromarray(self.stegImage)
        self.stegImage = self.hide(self.origImage, plainText)
        self.stegImage.save("secret.png")

        self.resultLbl.SetLabel("Message successfully encoded.")



    def DecodeEratosthenes(self, evt):
        clear_message = lsbset.reveal(self.imagePath, generators.eratosthenes())
        print(generators.eratosthenes())
        self.resultLbl.SetLabel(clear_message)
        
    def onOpenFileBtn(self, evt): 
      wildcard = "Image File (*.png; *.jpg; *.bmp; *.gif)|*.png;*.jpg;*.bmp;*.gif"
      dlg = wx.FileDialog(self, message="Choose an image file", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    



      #wildcard = "Text Files (*.txt)|*.txt" 
      #dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, wx.FD_OPEN)
		
      if dlg.ShowModal() == wx.ID_OK:
         self.imagePath = dlg.GetPath()
         #self.plainText.SetValue(dlg.GetPath())
         print (dlg.GetPath())
         self.ImagePathLbl.SetLabel(dlg.GetPath())
         self.ImagePathLbl.SetForegroundColour('red')
         copyfile(self.imagePath, "steg_img/steg_img.png")
         self.image.LoadFile("steg_img/steg_img.png")
         img = self.image
         img.Rescale(500, 500)
         self.picture.SetBitmap(wx.Bitmap(img))
         self.picture.SetSize(300,300)
         self.picture.SetPosition(wx.Point(420,70))
         
         

         

         
        

            
                
        

        
            
             
        
        
               

         #self.picture = wx.StaticBitmap(self.panel1, size=(100,100),pos=(100,100))
         
         #self.picture.SetSize(80,20)
         #self.picture = wx.StaticBitmap(self.panel1, -1, wx.Bitmap(self.image), size=(50, 50))
         
         #f = open(dlg.GetPath(), 'r') 
			
         #with f: 
         #   data = f.read() 
         #   self.text.SetValue(data)
         
      dlg.Destroy() 

    def onChoice(self, evt):
        choice = self.choice.GetStringSelection()
        method = getattr(self, "on_%s" % choice)
        method()

    def on_HeaderFile(self):
        print ("You chose test_A!")
        self.Bind(wx.EVT_BUTTON, self.EncodeExifHeader, id=self.encodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.DecodeExifHeader, id=self.decodeBtn.GetId())
    
    def on_LSB(self):
        print ("You chose test_B!")
        self.Bind(wx.EVT_BUTTON, self.onEncodeBtn, id=self.encodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.onDecodeBtn, id=self.decodeBtn.GetId())

    def on_RedPortionPixel(self):
        print ("You chose test_C!")
        self.Bind(wx.EVT_BUTTON, self.EncodeRedPortion, id=self.encodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.DecodeRedPortion, id=self.decodeBtn.GetId())

    def on_Eratosthenes(self):
        print ("You chose test_D!")
        self.Bind(wx.EVT_BUTTON, self.EncodeEratosthenes, id=self.encodeBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.DecodeEratosthenes, id=self.decodeBtn.GetId())
       
    def on_Steganalyse(self):
        print ("You chose test_E!")
        self.Bind(wx.EVT_BUTTON, self.doMe, id=self.decodeBtn.GetId())        


ex = wx.App()
stegInterface = StegInterface(None)
ex.MainLoop()    

'''
def main():
    ex = wx.App()
    stegInterface = StegInterface(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()
'''
