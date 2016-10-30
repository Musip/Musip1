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

def sequence_alignment(array1, array2, padding):
	height = len(array1)
	width = len(array2)
	result_matrix = [[0 for x in range(width)] for y in range(height)]

	for i in range(height):
		result_matrix[0][i] = i;

	for j in range(width):
		result_matrix[j][0] = j;

	for i in range(height):
		for j in range(width):
			match = 0 if abs(array1[i] - array2[j]) < padding else 1
			result_matrix[i][j] = min(match + result_matrix[i-1][j-1], \
									  1 + result_matrix[i-1][j], \
									  1 + result_matrix[i][j-1])

	return result_matrix[height-1][width-1]














