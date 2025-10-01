# pixcompress

## Simple image compression tool that creates compressed copies while keeping originals intact.

Effortlessly compress images with pixcompres an easy, fast, and reliable tool for shrinking JPEG, PNG, and GIF files while preserving quality.

## key Points
* Fast compression for JPEG, PNG, and GIF images

* Maintains image quality while reducing file size

* Batch processing: compress multiple files at once

* Provides clear error messages for common issues

* Easy command-line and Python API usage

* Suited for web, mobile, and personal projects

* Open source and customizable



## Install
install using pip(Python Package Manager):

```bash
# Using pip
pip install pixcompress
```

Or clone the repo and install locally:

```bash
git clone https://github.com/ruskaruma/pixcompress.git
cd pixcompress
pip install .

```


## Usage

Compress any image file:

```bash
pixcompress photo.jpg
#Creates: photo_compressed.jpg
```
### Example: Compress a Single JPG Image (Default Quality)

Command:
```bash
pixcompress sample.jpg
```


Output:
- Creates: `sample_compressed.jpg`
- Original file size: approx.977 KB
- Compressed file size: approx. 307 kB
- (63.0% reduction)

| Original Image | Compressed Image |
| -------------- | ---------------- |
| ![Original](pixcompress/images/Scanned_20251001_110320_page-0001.jpg) | ![Compressed](pixcompress/images/Scanned_20251001_110320_page-0001_compressed.jpg) |

 

```bash
pixcompress image.png --quality 70
#Creates: image_compressed.png with 70% quality
```
### Example: Compress a PNG Image with Custom Quality

Command:
```bash
pixcompress logo.png --quality 70
```


Output:
- Creates: `logo_compressed.png` with 70% quality
- Original file size: approx. 500KB
- Compressed file size: approx. 300KB


| Original Image                | Compressed Image              |
|------------------------------|------------------------------|
| ![Original]() | ![Compressed]() |


```bash
pixcompress large.jpg --max-width 1920 --max-height 1080
#Resizes and compresses to max 1920x1080
```
### Example: Resize and Compress an Image

Command:
```bash
pixcompress banner.jpg --max-width 1920 --max-height 1080
# Resize and compress an image to max dimensions 1920x1080
```


Output:
- Resizes image to max dimensions 1920x1080 and compresses
- Original file size: approx. 5MB
- Compressed file size: approx. 2MB

| Original Image                | Compressed Image              |
|------------------------------|------------------------------|
| ![Original]() | ![Compressed]() |


```bash
pixcompress photo.jpg --output compressed_photo.jpg
#Custom output filename
```

### Example: Compress and Specify Custom Output Filename

Command:
```bash
pixcompress photo.jpg --output photo_small.jpg
```


Output:
- Creates: `photo_small.jpg`
- Original file size: approx. 3MB
- Compressed file size: approx. 1.5MB


| Original Image                | Compressed Image              |
|------------------------------|------------------------------|
| ![Original]() | ![Compressed]() |




## Common Use Cases (FAQ)

**Q: Why compress images with pixcompress?**  
A: Reduce file sizes to speed up websites and apps without losing quality.

**Q: Can I compress multiple images at once?**  
A: Yes, batch processing lets you optimize entire folders quickly.

**Q: Does it resize images too?**  
A: You can set max width and height to resize before compressing.

**Q: Which image formats are supported?**  
A: JPEG, PNG, and GIF.

**Q: What if I try to compress a corrupted or unsupported file?**  
A: pixcompress shows clear error messages to help you fix it.

**Q: Can I use pixcompress in my automation workflows?**  
A: Absolutely—you can run commands in scripts or use the Python API.

**Q: Is it good for personal photo collections?**  
A: Yes, it’s great for saving disk space on your computer or cloud.

## Options

- `--quality, -q`: Compression quality (0-100, default: 85)
- `--max-width`: Maximum width in pixels (0 = no limit)
- `--max-height`: Maximum height in pixels (0 = no limit)
- `--output, -o`: Custom output filename

## Error Handling Examples

Command:
```bash
pixcompress non_existent.jpg
```


Output:
- Error: File not found. Please check the file path.

Command:
```bash
pixcompress corrupted_image.png
```


Output:
- Error: Cannot process the image. The file may be corrupted or in an unsupported format.

## Integration with Other Tools

- Can be used as a Python library to compress images programmatically
- Can be integrated into web servers or batch processes using shell commands
- Compatible with cloud storage tools for automated image optimization

## Troubleshooting

- Confirm the image file path and name are correct
- Supported formats: JPEG, PNG, and WebP
- Check write permissions in the output directory
- Use valid options values to avoid errors

## Future Improvements

I have big plans for pixcompress! Here are some features I'm working on:

- **Batch processing**: Compress multiple images at once
- **Format conversion**: Convert between JPEG, PNG, WebP automatically
- **Smart compression**: AI-powered quality optimization
- **GUI interface**: User-friendly desktop application
- **Cloud integration**: Direct upload to cloud storage services


## Contributing

pixcompress is an open-source project and we welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better for everyone.

### How to Contribute

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request

### Ideas for Contributors

- Add support for more image formats  
- Improve compression algorithms  
- Add command-line options  
- Write tests  
- Improve documentation  
- Create examples and tutorials

I'm excited to see what the community builds with pixcompress!

## License

MIT