#!/usr/bin/env python
# Program : tesseract-automation.py
# Version : 1.6
# Use : 
# tesseract-automation.py is a program created to select a pdf or a picture and convert it into text.
# tesseract-automation.py makes use of tesseract and only creates commandlines to automate things.
# Dependencies : 
# This version is used for the dutch language (-l nld).
# This program only works if tesseract-ocr tesseract-ocr-nld is installed on your computer.
# If you want another language install the language and change the commandline in this program to your needs !!!
# Perhaps other programs have to be installed aswell for example : imagemagick
# Also make sure you have installed the desired python-modules.
# How to run :
# Make the program executable, dubbleclick and choose open in terminal.
# You can run it also directly from the terminal with : python tesseract-automation.py
# Or run it from the terminal with : ./tesseract-automation.py
#
# Author : Folkert van der Meulen
# Date   : 26/06/2019
#
# Copyright 2019 Folkert van der Meulen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------

import Tkinter as tk
import tkFileDialog
import time
import os

## get pdf or picture for use in commandline
root = tk.Tk()
root.withdraw()
initialdirectory = '/home/pi/Documents'
pdf0or0picturefile = tkFileDialog.askopenfilename(initialdir = initialdirectory, filetypes=[('Supported types',('.pdf','.jpg','.png','.tif'))], title='Load pdf or picture')
extension = pdf0or0picturefile.split(".", pdf0or0picturefile.count("."))[1]
output0directory = pdf0or0picturefile.split(".", pdf0or0picturefile.count("."))[0]
print "\n"
print "program uses this file:"
print pdf0or0picturefile
print "\n"

if extension == 'pdf':
   print "---------------"
   print "  file is pdf"
   print "---------------"
   print "\n"
   mkdir0output0directory = 'mkdir ' + output0directory
   os.system(mkdir0output0directory)

   # Extract jpg's from pdf's. Quick and dirty. Between markers (#-), Credits to Ned Batchelder :
   # https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html
   #-
   pdf = open(pdf0or0picturefile, "rb").read()

   startmark = "\xff\xd8"
   startfix = 0
   endmark = "\xff\xd9"
   endfix = 2
   i = 0

   njpg = 0
   while True:
       istream = pdf.find("stream", i)
       if istream < 0:
           break
       istart = pdf.find(startmark, istream, istream+20)
       if istart < 0:
           i = istream+20
           continue
       iend = pdf.find("endstream", istart)
       if iend < 0:
           raise Exception("Didn't find end of stream!")
       iend = pdf.find(endmark, iend-20)
       if iend < 0:
           raise Exception("Didn't find end of JPG!")
     
       istart += startfix
       iend += endfix
       print "JPG %d from %d to %d" % (njpg, istart, iend)
       jpg = pdf[istart:iend]
       jpgfile = file(output0directory + "/Pagina%d.jpg" % njpg, "wb") 
       jpgfile.write(jpg)
       jpgfile.close()
     
       njpg += 1
       i = iend
   #-

   #get filenames in directory in textfile
   os.system('ls ' + output0directory + ' > ' + output0directory + '/ls-output.txt') 

   #read textfile lines and convert jpg in txt
   lines = [line.rstrip('\n') for line in open(output0directory + '/ls-output.txt')]

   for file in lines:
      result = file.startswith('Pagina')
      if result == True:
         time.sleep(1)
         txtfile = file.split(".", file.count("."))[0]
         cmd_run = 'tesseract  -l nld "%s/%s" "%s/%s"' %(output0directory,file,output0directory,txtfile)
         #print lines
         #print cmd_run
         os.system(cmd_run)

else:
   print "---------------"
   print "file is picture"
   print "---------------"
   print "\n"
   pdf0or0picturefileTXT = pdf0or0picturefile.replace("." + extension,"")
   cmd_run_emu = 'tesseract "%s" "%s" -l nld' %(pdf0or0picturefile,pdf0or0picturefileTXT)
   #print cmd_run_emu
   os.system(cmd_run_emu)

#read variable exit, after input the program stops 
print "\n"
print "File is converted to text !"
print "\n"
exit = raw_input("enter to exit :")