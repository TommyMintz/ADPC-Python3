#!/usr/bin/python
#
#The Algorithmic Digital Photo Collage
#Select photos and alpha channels to create collage
#
#Run With Python3  --- note: Uses PIL library 
#
#http://tommymintz.com/adpc/
#
#Released under the GNU General Public Liscence
#
#May 2022
#
#ver 2022.5.27
#
#with call_reversecollage() function called with 'r'
#
# run a loop of alphachannels, allow time for preview and editing of alpha
#  then run collage as seperate loop
#

import numpy
import sys
import os
import subprocess
import time
from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
from PIL import ImageOps
import shutil

#global variables
passedvalue = 1


#set directory. run first
def setdir():
    print('current directory is', os.getcwd())
    print('what directory?') 
    try:
        s = input()
        os.chdir(s)
        print (os.getcwd())
    except:
        print("Directory not exists.")
        os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        print(os.getcwd())
    return s

# run second sets an image for the base    
def setbase(): 
  try:	
    print('in def setbase')
    filenum = str(passedvalue)
    base = Image.open('photo%s.jpg' %filenum)
    subprocess.call (['cp photo%s.jpg tempbase.jpg' %filenum], shell = True) 
  except:
    print('error in making tempbase')
  try:
    subprocess.call (['cp tempbase.jpg collage%s.jpg' %filenum], shell = True)
    print('ran copy command in set base to generate tempbase.jpg and collage%s.jpg' %filenum)
  except:
    print(shutil.Error)
  print('attempting to make blur of base') 
  try:
    tempbase = Image.open('tempbase.jpg')
    print('tempbase base made through Image.open', tempbase)
  except:
    print('error in collage set base') 
  try:
    print('trying to blur the base')
    blurbase = tempbase.filter(ImageFilter.BLUR)
  except:
    print('problem blurring base', e)
  try:
    print('trying to save base')
    blurbase.save('blurbase.jpg')
    print('tempbase.jpg saved blurred')
  except:
    print('problem saving base', e)

def newbase():
  # activated by 'n'  saves a file called blurbase.jpg. Does not overwrite collage
 
  print('in def newbase')
  #filenum = input('What # for newbase?')
  #base = Image.open('photo%s.jpg' %filenum)
  #subprocess.call (['cp photo%s.jpg blurbase.jpg' %filenum], shell = True)
 
  try:
    filenum = input('what # photo to set to blurbase.jpg?') or str(passedvalue)
    tempblurbase = Image.open('photo%s.jpg' %filenum)
    print('tempblurbase base made through Image.open', tempblurbase)
  except:
    print ('error in newbase') 
  try:
    print ('trying to blur the base')
    blurbase = tempblurbase.filter(ImageFilter.BLUR)
  except:
    print('problem blurring base')
  try:
    print('trying to save base')
    blurbase.save('blurbase.jpg')
    os.system('say "blur base saved"')
    print('blurbase.jpg saved')
  except:
    print('problem saving glurbase.jpg')
  

#create alphachannel and save and display triggered with 'm'
def alphachannel():
  filenum = str(passedvalue)
  layer = Image.open('photo%s.jpg' %filenum)
  #alpha = Image.open('alphaeval%s.jpg' %filenum)
  print('blurring  the new layer.')
  blurphoto = layer.filter(ImageFilter.BLUR)
  print('making  alphachannel')
  blurbase = Image.open('blurbase.jpg')
  print('blurbase opened')
  alphachannel = ImageChops.difference(blurbase, blurphoto)
  print('images being compared')
  alphachannel = ImageOps.grayscale(alphachannel)
  alphachannel = Image.eval(alphachannel, lambda px:0 if px <15 else 255)
  print ('alphachannel generated')
  print ('alphachannel blurring')
  alphachannel = alphachannel.filter(ImageFilter.BLUR)
  alphachannel.convert('1')
  alphachannel.save('alphaeval%sM.jpg' %filenum)
  #try:
    #print('trying to display alphaeval%sM.jpg in preview' %filenum)
    #print (os.getcwd())
    #subprocess.call (['open', os.getcwd(),'alphaeval%sM.jpg' %filenum])
    #os.system('say "alpha channel %s ready."' %filenum)
    #justwaiting = input('ready to continue?')
  #except:
  	#print 'back from trying to show alphachannel'

#collage triggered with 'c' increments passed vaue  +1
def collage():
  global passedvalue
  alphachannum = str(passedvalue) 
  localalphachannel = Image.open('alphaeval%sM.jpg' %alphachannum)
  collage = Image.open('tempbase.jpg')
  layer = Image.open('photo%s.jpg' %alphachannum)  
  #use alphachannel to mask newphoto over oldcollage and save
  collage.paste(layer, None, localalphachannel)
  
  passedvalue += 1 
  print('passed value incremented. now', passedvalue)
  print('saving collage ', passedvalue)  

  filenum = str(passedvalue)
  collage.save('collage%sM.jpg' %filenum)
  print('collage%sM.jpg saved' %filenum)   
  collage.save('tempbase.jpg') 

  print('done making new collage') 

def alphachannels():
  try:  
    #setbase()
    global passedvalue
    print ('passedvalue is',passedvalue)
    passedvalue = int(input('what # for for  base?'))
    setbase()
    passedvalue = int(input('what # for for  1st photo?'))
    rangeofphotos = int(input('what # for last photo?'))
    while (int(passedvalue) <= int(rangeofphotos)):  
      alphachannel()     
      print('passed value is',passedvalue)  
      passedvalue += 1 
      print('passed value is',passedvalue)
  except:
      print('program problem in auto loop')
  os.system('say "the alpha channels are ready now."')
  
  
def autocollage():
  try:  
    #setbase()
    global passedvalue
    print('passedvalue is',passedvalue)
    passedvalue = int(input('what # for for  base?'))
    setbase()
    passedvalue = int(input('what # for for  1st photo?'))
    rangeofphotos = int(input('what # for last photo?'))
    while (int(passedvalue) <= int(rangeofphotos)):  
      print('passed value is',passedvalue)  
      collage()
      print('passed value is',passedvalue) 
    try:
      os.system('say "done"')
    except:
      print('program problem in using audio', e)
  except:
      print('program problem in auto loop', e)
      


def shootmanual(): 
  print('in shootmanual(): calling collage()')
  collage()
  print('passed back to shootmanual()')


def reversecollage():
  global passedvalue
  alphachannum = str(passedvalue) 
  localalphachannel = Image.open('alphaeval%sM.jpg' %alphachannum)
  collage = Image.open('tempbase.jpg')
  layer = Image.open('photo%s.jpg' %alphachannum)  
  #use alphachannel to mask newphoto over oldcollage and save
  collage.paste(layer, None, localalphachannel)
  
  passedvalue -= 1 
  print('passed value incremented. now', passedvalue)
  print('saving collage ', passedvalue)

  filenum = str(passedvalue)
  collage.save('collage%sM.jpg' %filenum)
  print('collage%sM.jpg saved' %filenum)
  collage.save('tempbase.jpg') 

  print('done making new collage')


def call_reversecollage():
  try:  
    #setbase()
    global passedvalue
    print('passedvalue is',passedvalue)
    passedvalue = int(input('what # for for  base?'))
    setbase()
    passedvalue = int(input('what # for for  1st photo to begin couting down from?'))
    rangeofphotos = int(input('what # for last photo?'))
    while (int(passedvalue) >= int(rangeofphotos)):  
      print ('passed value is',passedvalue)  
      reversecollage()
      print ('passed value is',passedvalue)  
    try:
      os.system('say "done"')
    except:
      print('program problem in using audio')
  except:
      print('program problem in auto loop')





#check to see if button has been pressed
def checkbuttons():
  try:
    buttonpushed = input("Next? s for dir, a for alphachanels, c for collage ")
    #buttonpushed = buttonpushed.rstrip()
    if buttonpushed in['q', 'Q']:
      sys.exit()
    #add layer with m
    elif buttonpushed in ['m', 'M']:
      print('caught m to make alpha channel()')
      alphachannel()
    #set directory mode with a
    elif buttonpushed in ['s']:
      print('setting directory')
      setdir()
    #generate new base with b
    elif buttonpushed in ['n']:
      newbase() 
    elif buttonpushed in ['b']:
      print('caught b trying to generate starting base with setbase()')
      setbase()  
    elif buttonpushed == 'p':
      printer(numgen.imgno)
    elif buttonpushed in ['c']:
      autocollage()  
    elif buttonpushed in ['a']:
      alphachannels()  
    elif buttonpushed in ['r']:
      call_reversecollage()
    else:
      print('not a valid key')
  except:
    print ('ADPC caught Program problem in check buttons')

def startprogram():

  while True:
    print('We are good to go! Autocollager v. 2022.5.27')
    c = checkbuttons()
    #print 'in startprogram about to time.sleep(0.1)'
    time.sleep(0.1)
      
go = startprogram()
