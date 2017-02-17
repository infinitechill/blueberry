import Tkinter, Tkconstants, tkFileDialog
from PIL import Image, ImageTk
import numpy as np
import wave

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

from array import array
import sys, subprocess, os


class MyBlueberryMenu(Tkinter.Frame):
	def __init__(self, root):
	    Tkinter.Frame.__init__(self, root)
	    background_image=Tkinter.PhotoImage('image.jpg')
	    background_label = Tkinter.Label(self, image=background_image)
	    background_label.place(x=0, y=0, relwidth=1, relheight=1)
	    # options for buttons
	    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
	    # define buttons
	    BlueberryButton = Tkinter.Button(self, text="GO!", command=self.startprocess)
	    BlueberryButton.grid(row=0, column=0)
	    # define options for opening or saving a file
	    self.file_opt = options = {}
	    options['defaultextension'] = '.wav'
	    options['filetypes'] = [('jpg files', '.jpg'), ('wav files', '.wav')]
	    options['initialdir'] = 'C:\\'
	    options['initialfile'] = 'blueberry.wav'
	    options['parent'] = root
	    options['title'] = 'Blueberry 1.0'

	def askopenfilename(self):
	    # get filename
	    filename = tkFileDialog.askopenfilename(**self.file_opt)
	    # open file on your own
	    if filename:
			return open(filename, 'r')

	def asksaveasfilename(self):
	    filename = tkFileDialog.asksaveasfilename(**self.file_opt)
	    # open file on your own
	    if filename:
			return open(filename, 'w')
      
	def make_wav(self, image_name, output_name):
	    # load input image
		image = mpimg.imread(image_name)
		image = np.sum(image, axis = 2).T[:, ::-1]
		image = image**3 # ???
		w, h = image.shape
		# fourier transform, normalize, remove DC bias
		stream = np.fft.irfft(image, h*2, axis=1).reshape((w*h*2))
		stream -= np.average(stream)
		stream *= (2**15-1.)/np.amax(stream)
		stream = array("h", np.int_(stream)).tostring()
		# save output
		output_file = wave.open(output_name, "w")
		output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
		output_file.writeframes(stream)
		output_file.close()
		return output_name
  
	# user clicked go
	def startprocess(self):
		# get full input file path
		inputfilename = tkFileDialog.askopenfilename(**self.file_opt)
		# get full output file path
		outputfilename = tkFileDialog.asksaveasfilename(**self.file_opt)
		# open file
		if inputfilename:
			self.make_wav(inputfilename, outputfilename)
			if outputfilename:
				if sys.platform.startswith('darwin'):
					subprocess.call(('open', outputfilename))
				elif os.name == 'nt':
					os.startfile(outputfilename)
				elif os.name == 'posix':
					subprocess.call(('xdg-open', outputfilename))

# build gui and wait for user-driven event      
if __name__=='__main__':
    root = Tkinter.Tk()
    PILFile = Image.open("image.jpg")
    Image = ImageTk.PhotoImage(PILFile) # <---
    ImageLabel = Tkinter.Label(root, image=Image)
    ImageLabel.image = Image
    ImageLabel.pack()
    MyBlueberryMenu(root).pack()
    root.mainloop()
