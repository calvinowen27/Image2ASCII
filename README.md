# Image2ASCII

# Usage  
To use, make sure you have downloaded the image2ascii.py python file. With the image you want to convert in the same directory, run the python file from the terminal using '$ python image2ascii.py [input file name] [optional mode]  
  
# Valid modes  
  - mean (uses mean value across RGBA channels to determine darkness)
  - min (uses min value across RGBA channels to determine darkness)
  - max (uses max value across RGBA channels to determine darkness)
  - red (uses only red value as darkness)
  - green (uses only green value as darkness)
  - blue (uses only blue value as darkness)

# Dependencies
Requires Pillow and numpy libraries to be installed for the latest version of Python.
