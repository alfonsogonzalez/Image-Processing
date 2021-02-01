# Image processing scripts
# Accepts all types of rgb images

Uses:

# Always include input image and output path. In examples, these two flags will be omitted
python process.py --img=/path/to/input/image.jpg --out=/path/to/processed/image.jpg


#To alter rgb values individually, use:
python process.py --alter-colors r g b
# input integers (positive or negative) for r, g, b


# To make image negative, use:
python process.py --neg


# To make image black and white, use:
python process.py --bnw


# To blur entire image, use:
python process.py --blur --reach=num
# num is an integer. use numbers from 1 to 7. higher numbers are blurrier and take longer to process


# To blur entire image except for a circular area, use:
python process.py --blur-spotlight --center x y --radius=num
# This will leave one area untouched, then gradually blur more as the distance from center area increases


# To create a spotlight at a spot in the imagae, use:
python process.py --spotlight --center x y --radius=num
# x and y are both integers and are coordinates for center of spotlight. x = 0 is the left side of the image
# and y = 0 is the top of the image. num is an integer for the radius of the spotlight (in pixels)


# To brighten or darken image by certain amount, use:
python process.py --brighten=num
# num is an integer. if positive, image will brighten. if negative, image will darken`x
