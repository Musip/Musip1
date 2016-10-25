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

loader = essentia.standard.MonoLoader(filename='sample/hill_sample.mp3')
audio = loader() # load the music


window = essentia.standard.Windowing(type = 'hann') # window function
spectrum = essentia.standard.Spectrum()  # spectrum function
pitch_yin_fft = essentia.standard.PitchYinFFT() # pitch extractor
pitch_saliennce = essentia.standard.PitchSalience()

index = 0
pitches = []
tones = []

# Extract pitches for each frame
for frame in essentia.standard.FrameGenerator(audio, frameSize = 2048, hopSize = 512):

	sample_spectrum = spectrum(window(frame))
	pitch, pitch_confidence = pitch_yin_fft(sample_spectrum)

	maxAmp = 0
	for amp in sample_spectrum:
		currentAmp = abs(amp)
		if currentAmp > maxAmp:
			maxAmp = currentAmp

	if pitch_confidence < 0.8:
		pitches.append(0.0)
	else:
		pitches.append(pitch)

	index = index + 1

# for pitch in pitches:
# 	if pitch != 0.0:
# 		print pitch

plt.plot(range(len(pitches)), pitches, label='pitch')
plt.show()




