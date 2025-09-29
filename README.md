# pixcompress

Simple image compression tool that creates compressed copies while keeping originals intact.

## Install

```bash
pip install pixcompress
```

## Usage

Compress any image file:

```bash
pixcompress photo.jpg
#Creates: photo_compressed.jpg

pixcompress image.png --quality 70
#Creates: image_compressed.png with 70% quality

pixcompress large.jpg --max-width 1920 --max-height 1080
#Resizes and compresses to max 1920x1080

pixcompress photo.jpg --output compressed_photo.jpg
#custom output filename
```

## Options

- `--quality, -q`: Compression quality (0-100, default: 85)
- `--max-width`: Maximum width in pixels (0 = no limit)
- `--max-height`: Maximum height in pixels (0 = no limit)  
- `--output, -o`: Custom output filename

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
