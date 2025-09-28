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
# Creates: photo_compressed.jpg

pixcompress image.png --quality 70
# Creates: image_compressed.png with 70% quality

pixcompress large.jpg --max-width 1920 --max-height 1080
# Resizes and compresses to max 1920x1080

pixcompress photo.jpg --output compressed_photo.jpg
# custom output filename
```

## Options

- `--quality, -q`: Compression quality (0-100, default: 85)
- `--max-width`: Maximum width in pixels (0 = no limit)
- `--max-height`: Maximum height in pixels (0 = no limit)  
- `--output, -o`: Custom output filename

## License

MIT
