from PIL import Image
import numpy as np
import sys
import os

conversion = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
alpha_conversion = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%%B@$'

def convert_to_ascii(pxs, mode, has_alpha):
	# parse mode
	match mode:
		case "mean":
			modified_pxs = pxs.mean(axis=2)
		case "min":
			modified_pxs = pxs.min(axis=2)
		case "max":
			modified_pxs = pxs.max(axis=2)
		case "red":
			modified_pxs = pxs[:, :, 0]
		case "green":
			modified_pxs = pxs[:, :, 1]
		case "blue":
			modified_pxs = pxs[:, :, 2]
		case _:
			raise Exception('Invalid mode argument. Mode can be mean, min, max, red, blue, or green.')
	
	rows, cols = pxs.shape[:2]
	
	# Only look at every other row in image due to difference in height and width of ascii chars
	result = ['']*(rows//2)

	for r in range(0, rows, 2):
		for c in range(cols):
			# If alpha exists it has priority on determining darkness
			if has_alpha and pxs[r, c, 3] < 255:
				alpha_idx = int(float(pxs[r, c, 3] / 255) * (len(alpha_conversion) - 1))
				result[r//2] += alpha_conversion[alpha_idx]				
			else: # otherwise get relative darkness from conversion scale
				idx = int(float(modified_pxs[r, c] / 255) * (len(conversion) - 1))
				result[r//2] += conversion[idx]

	return result

if __name__ == '__main__':
	n_args = len(sys.argv)

	# make sure arguments are valid
	assert n_args >= 2, 'Invalid arguments. 1 input file path argument required.'
	assert n_args <= 3, 'Invalid arguments. Cannot have more arguments than input file and sampling mode'
	assert os.path.exists(sys.argv[1]), 'Invalid input file path. File does not exist'
	
	# get mode argument
	mode = "mean"
	if n_args == 3:
		mode = sys.argv[2]

	# set input and ouput paths
	inpath = sys.argv[1]
	outpath = inpath[:-4] + f'_{mode}_out.txt'

	# open image
	image = Image.open(inpath)

	# open image and insert into 2D array
	has_alpha = inpath[-4:] == '.png'

	if has_alpha: # alpha means 4 channels instead of 3
		pxs = np.array(image.getdata()).reshape(image.size[1], image.size[0], 4)
	else:
		pxs = np.array(image.getdata()).reshape(image.size[1], image.size[0], 3)

	ascii_img = convert_to_ascii(pxs, mode, has_alpha)

	# write ascii text to outfile
	with open(outpath, 'w+') as outfile:
		outfile.writelines('\n'.join(ascii_img))