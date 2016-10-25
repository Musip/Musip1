import matplotlib.pyplot as plt

def draw_plot(frames, window, spectrum, pitch_yin_fft, pitch_saliennce):
	# index = 0
	pitches = []
	tones = []

	# Extract pitches for each frame
	for frame in frames:
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

		# index = index + 1

	plt.plot(range(len(pitches)), pitches, label='pitch')
	plt.show()
