import random


# The classic string-between
def strbet(text, start, end):
	start_str = text.find(start)

	if start_str == -1:
		return None

	end_str = text.find(end, start_str)

	if not end_str:
		return None

	start_str += len(start)
	return text[start_str:end_str]


def rndk(charset):
	charset = list(charset)
	random.shuffle(charset)
	return ''.join(charset)
