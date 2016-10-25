from essentia.standard import MonoLoader, FrameGenerator, Windowing, \
Spectrum, PitchYinFFT, PitchSalience

import essentia.streaming
import argparse

from Comparator import draw_plot

def _set_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--source', help='the file to process', required=True)
	parser.add_argument('-d', '--destination', help='the file to compare with', required=True)

	args = parser.parse_args()

	return args

# Essentia has a selection of audio loaders:
#
#  - AudioLoader: the basic one, returns the audio samples, sampling rate and number of channels
#  - MonoLoader: which returns audio, down-mixed and resampled to a given sampling rate
#  - EasyLoader: a MonoLoader which can optionally trim start/end slices and rescale according
#                to a ReplayGain value
#  - EqloudLoader: an EasyLoader that applies an equal-loudness filtering on the audio
def _loader(path):
	loader = MonoLoader(filename = path)
	audio = loader() # load the music

	return audio

def main():
	args = _set_arguments()

	source_audio = _loader(args.source)
	destination_audio = _loader(args.destination)

	source_frame = FrameGenerator(source_audio, frameSize = 2048, hopSize = 512)
	destination_frame = FrameGenerator(destination_audio, frameSize = 2048, hopSize = 512)

	window = Windowing(type = 'hann') # window function
	spectrum = Spectrum()  # spectrum function
	pitch_yin_fft = PitchYinFFT() # pitch extractor
	pitch_saliennce = PitchSalience()

	draw_plot(source_frame, window, spectrum, pitch_yin_fft, pitch_saliennce)

if __name__ == '__main__':
	main()
