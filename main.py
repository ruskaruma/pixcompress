from PIL import Image

def compress_image(input_path, output_path, output_quality):
    '''
    Compresses an image and saves it to the output path.

    Args:
        input_path: The path to the input image.
        output_path: The path to save the compressed image.
        quality: The compression quality (0-100).
    '''

    img = Image.open(input_path)
    print(img)
    img.save(output_path, optimize = False, quality = int(output_quality))

inputPath = input("Enter Local Path to the Input Image : ")
outputPath = input("Enter Output Path for the Image : ")
outputQuality = input("Enter Desired Quality of the Image (0-100) : ")

print("IP: ", inputPath, "OP: ", outputPath, "OQ: ", outputQuality, "\n")

compress_image(inputPath, outputPath, outputQuality)