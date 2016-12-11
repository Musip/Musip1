import matplotlib.pyplot as plt
import logging

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
	result_matrix = [[0 for x in range(width + 1)] for y in range(height + 1)]
	previous = [[(0, 0) for x in range(width + 1)] for y in range(height + 1)]

	for i in range(width+1):
		result_matrix[0][i] = i;

	for i in range(height+1):
		result_matrix[i][0] = i;

	# dp
	for i in range(height):
		for j in range(width):
			match = 0 if abs(array1[i] - array2[j]) <= padding else mismatch_penalty
			match_cost = match + result_matrix[i][j]
			gap1 = gap_penalty + result_matrix[i+1][j]
			gap2 = gap_penalty + result_matrix[i][j+1]
			min_cost = min(match_cost, gap1, gap2)
			result_matrix[i+1][j+1] = min_cost
			if min_cost == match_cost:
				previous[i+1][j+1] = (i, j)
			elif min_cost == gap1:
				previous[i+1][j+1] = (i+1, j)
			else:
				previous[i+1][j+1] = (i, j+1)

	match_result = []
	current = (height, width)
	current_i = current[0]
	current_j = current[1]
	array1_index = len(array1) - 1
	array2_index = len(array2) - 1

	# backtrack
	while array1_index != 0 and array2_index != 0:
		prev = previous[current_i][current_j]
		prev_i = prev[0]
		prev_j = prev[1]

		match = 0
		if current_i - prev_i == 1 and current_j - prev_j == 1:
			if abs(array1[array1_index] - array2[array2_index]) > padding:
				match = 1 # mismatch
			array1_index = array1_index - 1
			array2_index = array2_index - 1
		elif current_i - prev_i == 1:
			match = 3
			array1_index = array1_index - 1
		elif current_j - prev_j == 1:
			match = 2
			array2_index = array2_index - 1
		else:
			print "This should not happen."
		match_result.append(match)

		current = prev
		current_i = current[0]
		current_j = current[1]

	# calculate the gap left
	diff = array1_index - array2_index
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

	# This part needs some attention or fix

	start_index = 0
	end_index = len(match_result) - 1
	while start_index < len(match_result) and match_result[start_index] == 2:
		start_index = start_index + 1

	while end_index >= 0 and match_result[end_index] == 2:
		end_index = end_index - 1


	# return (result_matrix[height][width], match_result)
	return (result_matrix[height][width], match_result[start_index:end_index + 1])

def compare(source_frames, destination_frames, window, spectrum, pitch_yin_fft, \
	        padding, gap_penalty, mismatch_penalty, display, loudness):
	confidence_level = 0.75
	loudness_threshold = 0.3
	source_pitches = []
	destination_pitches = []

	# Extract pitches for each frame
	for source_frame in source_frames:
		l = loudness(source_frame)
		source_spectrum = spectrum(window(source_frame))
		source_pitch, source_pitch_confidence = pitch_yin_fft(source_spectrum)

		if source_pitch_confidence < confidence_level:
			source_pitches.append(0.0)
		else:
			if l < loudness_threshold:
				source_pitches.append(0.0)
			else:
				source_pitches.append(source_pitch)

	for destination_frame in destination_frames:
		l = loudness(destination_frame)
		destination_spectrum = spectrum(window(destination_frame))
		destination_pitch, destination_pitch_confidence = pitch_yin_fft(destination_spectrum)

		if destination_pitch_confidence < confidence_level:
			destination_pitches.append(0.0)
		else:
			if l < loudness_threshold:
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









