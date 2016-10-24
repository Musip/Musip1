import essentia.standard
import essentia.streaming

# pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

# Essentia has a selection of audio loaders:
#
#  - AudioLoader: the basic one, returns the audio samples, sampling rate and number of channels
#  - MonoLoader: which returns audio, down-mixed and resampled to a given sampling rate
#  - EasyLoader: a MonoLoader which can optionally trim start/end slices and rescale according
#                to a ReplayGain value
#  - EqloudLoader: an EasyLoader that applies an equal-loudness filtering on the audio
#
loader = essentia.standard.MonoLoader(filename='sample/two_tigers_sample.mp3')
audio = loader() # load the music

window = essentia.standard.Windowing(type = 'hann') # window function
spectrum = essentia.standard.Spectrum()  # spectrum function
pitch_yin_fft = essentia.standard.PitchYinFFT() # pitch extractor

index = 0
pitches = []

# Extract pitches for each frame
for frame in essentia.standard.FrameGenerator(audio, frameSize = 4096, hopSize = 512):
	sample_spectrum = spectrum(window(frame))
	pitch, pitch_confidence = pitch_yin_fft(sample_spectrum)
	pitches.append(pitch)
	index = index + 1


plt.plot(pitches)
plt.show()




