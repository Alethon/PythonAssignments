import os

def find(pattern):
	matches = []
	with open(os.path.join(DataPath, 'sequence.txt'), "r") as file:
		s = file.readline()
	for i in range(len(s) - len(pattern) + 1):
		discard = 0
		for j in range(len(pattern)):
			if not discard and str.isdigit(pattern[j]) and pattern[j] is not s[i:i+len(pattern)][j]:
				discard = 1
		if not discard:
			matches.append(s[i:i+len(pattern)])
	return matches

def product(nums):
	p = 1
	for i in nums:
		p = p * i
	return p

def getStreakProduct(sequence, maxSize, product):
	matches = []
	with open(os.path.join(DataPath, 'sequence.txt'), "r") as file:
		s = file.readline()
	for i in range(len(s) - len(pattern) + 1):
		discard = 0
		for j in range(len(pattern)):
			if not discard and str.isdigit(pattern[j]) and pattern[j] is not s[i:i+len(pattern)][j]:
				discard = 1
		if not discard:
			matches.append(s[i:i+len(pattern)])
	return matches

if __name__ == "__main__":
	DataPath = '/home/ecegridfs/a/ee364/DataFolder/Prelab01'
	find("X01X")
	
