import matplotlib.pyplot as plt

def draw_plot(frames, window, spectrum, pitch_yin_fft):
	# index = 0
	pitches = []

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

def sequence_alignment(array1, array2, padding, gap_penalty, mismatch_penalty):
	height = len(array1)
	width = len(array2)
	result_matrix = [[0 for x in range(width)] for y in range(height)]
	previous = [[(0, 0) for x in range(width)] for y in range(height)]

	for i in range(width):
		result_matrix[0][i] = i;

	for j in range(height):
		result_matrix[j][0] = j;

	# dp
	for i in range(height):
		for j in range(width):
			match = 0 if abs(array1[i] - array2[j]) <= padding else mismatch_penalty
			match_cost = match + result_matrix[i-1][j-1]
			gap1 = gap_penalty + result_matrix[i][j-1]
			gap2 = gap_penalty + result_matrix[i-1][j]
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

	# backtrack
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

	# calculate the gap left
	diff = current_i - current_j
	if diff == 0:
		match = 0 if abs(array1[0] - array2[0]) < padding else 1
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

	return (result_matrix[height-1][width-1], match_result)

def compare(source_frames, destination_frames, window, spectrum, pitch_yin_fft, \
	        padding, gap_penalty, mismatch_penalty, display):
	confidence_level = 0.3
	source_pitches = []
	destination_pitches = []

	# Extract pitches for each frame
	for source_frame in source_frames:
		source_spectrum = spectrum(window(source_frame))
		source_pitch, source_pitch_confidence = pitch_yin_fft(source_spectrum)

		if source_pitch_confidence < confidence_level:
			source_pitches.append(0.0)
		else:
			source_pitches.append(source_pitch)

	for destination_frame in destination_frames:
		destination_spectrum = spectrum(window(destination_frame))
		destination_pitch, destination_pitch_confidence = pitch_yin_fft(destination_spectrum)

		if destination_pitch_confidence < confidence_level:
			destination_pitches.append(0.0)
		else:
			destination_pitches.append(destination_pitch)

	min_cost, match_result = sequence_alignment(source_pitches, destination_pitches, padding, \
		                                        gap_penalty, mismatch_penalty)

	if display:
		display_result(source_pitches, destination_pitches, match_result)

	return (min_cost, match_result)

def display_result(source_pitches, destination_pitches, match_result):
	source_display = []
	destination_display = []

	source_index = 0
	destination_index = 0

	for match in match_result:
		if match == 0 or match == 1:
			source_display.append(source_pitches[source_index])
			destination_display.append(destination_pitches[destination_index])
			source_index = source_index + 1
			destination_index = destination_index + 1
		elif match == 2:
			source_display.append(0.0)
			destination_display.append(destination_pitches[destination_index])
			destination_index = destination_index + 1
		elif match == 3:
			destination_display.append(0.0)
			source_display.append(source_pitches[source_index])
			source_index = source_index + 1
		else:
			print "match result shouldn't contain {}.".format(match)

	plt.plot(range(len(source_display)), source_display, label='source_pitch')
	plt.plot(range(len(destination_display)), destination_display, label='destination_pitch')
	plt.show()









