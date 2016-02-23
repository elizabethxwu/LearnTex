import numpy as np
import cv2
	
def has_writing(pixelList, threshold):
	for pixel in pixelList:
		if pixel < threshold:
			return True
	return False

def get_lines_of_text(img):
	width = len(img[0])
	height = len(img)
	lineDimensions = []

	i = 0
	while i < height:
		top, bottom = 0,0
		row = img[i,:]
		if has_writing(row, 100):
			top = i
			j = i
			while(has_writing(row,100)):
				row = img[j,:]
				j+=1
			bottom = j
			i = j
			lineDimensions.append([top, bottom, 0, width])
		else:
			i+=1

	"""
	for aLine in lineDimensions:
		i = 0
		col = img[aLine[0]:aLine[1],i]
		while not has_writing(col,100):
			i+=1
			col = img[aLine[0]:aLine[1],i]
		aLine[2] = i-10
		print i

		i = width-1
		col = img[aLine[0]:aLine[1],i]
		while not has_writing(col,100):
			i-=1
			col = img[aLine[0]:aLine[1],i]
		aLine[3] = i+10
	"""

	return lineDimensions

def find_character_indices(line):

	width = len(line[0])
	height = len(line)
	characterIndices = []

	i = 0
	while i < width:
		start,end = 0,0
		col = line[:,i]
		if has_writing(col, 150):
			start = i
			j = i
			while(has_writing(col, 150)):
				col = line[:,j]
				j+=1
			end = j
			i = j
			characterIndices.append([start, end])
		else:
			i+=1

	for i in range(len(characterIndices)-1):
		if characterIndices[i+1][0] - characterIndices[i][1] > 30:
			characterIndices.insert(i+1, [characterIndices[i][1], characterIndices[i+1][0]])

	return characterIndices

def main():

	# load the image as a numpy array using openCV
	scanFilepath = 'scans/scan1.png'
	img = cv2.imread(scanFilepath, 0)

	"""
	cv2.destroyAllWindows()
	"""

	lineDimensions = get_lines_of_text(img)
	for lineDim in lineDimensions:
		cv2.imshow('z', img[lineDim[0]:lineDim[1],lineDim[2]:lineDim[3]])
		cv2.waitKey(0)
		characterIndices = find_character_indices(img[lineDim[0]:lineDim[1],lineDim[2]:lineDim[3]])
		for charIndex in characterIndices:
			cv2.imshow('z', img[lineDim[0]:lineDim[1],charIndex[0]:charIndex[1]])
			cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
