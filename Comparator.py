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
	previous = [[(0, 0) for x in range(width)] for y in range(height)]

	for i in range(height):
		result_matrix[0][i] = i;

	for j in range(width):
		result_matrix[j][0] = j;

	for i in range(height):
		for j in range(width):
			match = 0 if abs(array1[i] - array2[j]) <= padding else 1
			match_cost = match + result_matrix[i-1][j-1]
			gap1 = 1 + result_matrix[i][j-1]
			gap2 = 1 + result_matrix[i-1][j]
			min_cost = min(match_cost, gap1, gap2)
			result_matrix[i][j] = min_cost
			if min_cost == match_cost:
				previous[i][j] = (i-1, j-1)
			elif min_cost == gap1:
				previous[i][j] = (i, j-1)
			else:
				previous[i][j] = (i-1, j)

	match_result = []
	current = previous[height-1][width-1]
	current_i = current[0]
	current_j = current[1]

	while current_i != -1 and current_j != -1:
		x = current[0]
		y = current[1]
		prev = previous[x][y]
		prev_i = prev[0]
		prev_j = prev[1]

		match = 0
		if current_i - prev_i == 1 and current_j - prev_j == 1:
			if abs(array1[x + 1] - array2[y + 1]) > padding:
				match = 1 # mismatch
		elif current_i - prev_i == 1:
			match = 3
		elif current_j - prev_j == 1:
			match = 2
		else:
			print "This should not happen."
		match_result.append(match)

		current_i = prev_i
		current_j = prev_j
		current = prev

	diff = current_i - current_j
	if diff == 0:
		match = 0 if abs(rray1[0] - array2[0]) < padding else 1
		match_result.append(match)
	elif diff > 0:
		match = 0 if abs(array1[diff] - array2[0]) < padding else 1
		match_result.append(match)
		while diff > 0:
			match_result.append(3)
			diff = diff - 1
	else:
		match = 0 if abs(array1[0] - array2[diff] < padding) else 1
		match_result.append(match)
		while diff > 0:
			match_result.append(2)
			diff = diff - 1

	match_result.reverse()

	return result_matrix[height-1][width-1]

sequence_alignment([2,4,1,2,2,3],[4,1,2,1,4,3], 0.1)











