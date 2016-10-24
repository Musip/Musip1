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
# loader = essentia.standard.MonoLoader(filename='sample/two_tigers_sample.mp3')
loader_filtered = essentia.standard.MonoLoader(filename='sample/hill_sample_filtered.mp3')
# audio = loader() # load the music
audio_filtered = loader_filtered()

window = essentia.standard.Windowing(type = 'hann') # window function
spectrum = essentia.standard.Spectrum()  # spectrum function
pitch_yin_fft = essentia.standard.PitchYinFFT() # pitch extractor

index = 0
# pitches = []
pitches_filtered = []
frames = []

# Extract pitches for each frame
for frame_filtered in essentia.standard.FrameGenerator(audio_filtered, frameSize = 2048, hopSize = 512):
	# sample_spectrum = spectrum(frame)
	# pitch, pitch_confidence = pitch_yin_fft(sample_spectrum)
	# pitches.append(pitch)
	for f in frame_filtered:
		frames.append(f)

	sample_spectrum = spectrum(window(frame_filtered))
	pitch, pitch_confidence = pitch_yin_fft(sample_spectrum)

	if pitch_confidence < 0.8:
		print "{}: {}".format(pitch, pitch_confidence)
		pitches_filtered.append(0.0)
	else:
		pitches_filtered.append(pitch)

	index = index + 1

plt.plot(frames)
plt.show()

# plt.plot(range(len(pitches_filtered)), pitches_filtered, label='filtered')
# plt.plot(range(len(pitches)), pitches, label='original')
# plt.show()




