# first, we need to import our essentia module. It is aptly named 'essentia'!

import essentia

# as there are 2 operating modes in essentia which have the same algorithms,
# these latter are dispatched into 2 submodules:

import essentia.standard
import essentia.streaming

# pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
from pylab import plot, show, figure

# let's have a look at what is in there

# print dir(essentia.standard)

# you can also do it by using autocompletion in IPython, typing "essentia.standard." and pressing Tab

# Essentia has a selection of audio loaders:
#
#  - AudioLoader: the basic one, returns the audio samples, sampling rate and number of channels
#  - MonoLoader: which returns audio, down-mixed and resampled to a given sampling rate
#  - EasyLoader: a MonoLoader which can optionally trim start/end slices and rescale according
#                to a ReplayGain value
#  - EqloudLoader: an EasyLoader that applies an equal-loudness filtering on the audio
#

# we start by instantiating the audio loader:
loader = essentia.standard.MonoLoader(filename='sample/cannon.mp3')

# and then we actually perform the loading:
audio = loader()

# by default, the MonoLoader will output audio with 44100Hz samplerate

plot(audio[2*44100:3*44100])
show() # unnecessary if you started "ipython --pylab"