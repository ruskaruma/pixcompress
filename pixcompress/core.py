from pathlib import Path
from PIL import Image
import shutil
from typing import Union, Optional


def _ensure_dir(path: Path):
    """Ensure that the parent directory of the given path exists.  

    Creates all missing parent directories if they do not exist.
    
    Args:
        path (Path): The file path for which the parent directory should exist.
    
    Example:
        >>> _ensure_dir(Path("output/images/photo.jpg"))
        # Creates 'output/images' if it does not exist
    """
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_exif(img: Image.Image):
    """Retrieve the EXIF metadata from an image, if available.

    Args:
        img (Image.Image): PIL Image object.
    
    Returns:
        bytes or None: EXIF data as bytes if present, otherwise None.
    
    Example:
        >>> exif_data = _get_exif(Image.open("photo.jpg"))
        >>> type(exif_data)
        <class 'bytes'>
    """
    return img.info.get("exif", None)


def _resize_if_needed(img: Image.Image, max_size):
    """Resize an image to fit within max dimensions while preserving aspect ratio.

    Args:
        img (Image.Image): PIL Image object to resize.
        max_size (tuple or None): Maximum width and height as (max_width, max_height). 
                                  If None or any dimension is 0, no resizing occurs.
    
    Returns:
        Image.Image: The resized image, or original image if resizing was not needed.
    
    Example:
        >>> resized_img = _resize_if_needed(img, (800, 600))
        >>> resized_img.size
        (800, 450)
    """
    if not max_size:
        return img
    mx_w, mx_h = max_size
    if mx_w == 0 or mx_h == 0:
        return img
    w, h = img.size
    if w <= mx_w and h <= mx_h:
        return img
    img.thumbnail((mx_w, mx_h), Image.LANCZOS)
    return img


def compress(src: str,
             dst: str,
             quality: int = 85,
             max_size: Optional[tuple] = None,
             convert_to: Optional[str] = None,
             optimize: bool = True,
             preserve_exif: bool = False,
             progressive: bool = True,
             webp_lossless: bool = False) -> dict:
    """Compress a single image file.
    
    Args:
        src (str): Path to the source image file.
        dst (str): Path where the compressed image will be saved.
        quality (int, optional): Compression quality (1-100). Defaults to 85.
        max_size (tuple, optional): Maximum width and height to resize the image. Defaults to None (no resizing).
        convert_to (str, optional): Convert image to this format ('JPEG', 'PNG', 'WEBP'). Defaults to None (use original format).
        optimize (bool, optional): Whether to optimize the image. Defaults to True.
        preserve_exif (bool, optional): Whether to preserve EXIF metadata. Defaults to False.
        progressive (bool, optional): Save JPEG as progressive. Defaults to True.
        webp_lossless (bool, optional): Save WebP image in lossless mode. Defaults to False.
        
    Returns:
        dict: Dictionary containing:
            - "src" (str): Source file path.
            - "dst" (str): Destination file path.
            - "orig_size" (int): Original file size in bytes.
            - "new_size" (int): Compressed file size in bytes.
    Raises:
        FileNotFoundError: If the source file does not exist.
        Exception: If the image cannot be saved in its original format and fallback copy fails.
    Example:
        >>> compress("input.jpg", "output.jpg", quality=80, max_size=(800, 600))
        {'src': 'input.jpg', 'dst': 'output.jpg', 'orig_size': 204800, 'new_size': 102400}
    """
    src_p = Path(src)
    dst_p = Path(dst)
    if not src_p.exists():
        raise FileNotFoundError(f"Source not found: {src}")

    _ensure_dir(dst_p)

    with Image.open(src_p) as img:
        orig_size = src_p.stat().st_size

        #convert to RGB if needed
        if img.mode not in ("RGB", "RGBA", "L"):
            img = img.convert("RGB")

        img = _resize_if_needed(img, max_size)

        exif_bytes = _get_exif(img) if preserve_exif else None
        target = (convert_to or img.format or dst_p.suffix.replace(".", "")).upper()

        if target in ("JPG", "JPEG"):
            save_kwargs = {
                "format": "JPEG",
                "quality": int(quality),
                "optimize": optimize,
                "progressive": progressive,
            }
            if exif_bytes:
                save_kwargs["exif"] = exif_bytes
            img.save(dst_p, **save_kwargs)

        elif target == "WEBP":
            save_kwargs = {
                "format": "WEBP",
                "quality": int(quality),
                "lossless": webp_lossless,
                "method": 6,
            }
            img.save(dst_p, **save_kwargs)

        elif target == "PNG":
            if img.mode == "RGBA":
                img.save(dst_p, format="PNG", optimize=optimize)
            else:
                if quality < 90:
                    #reduce colors for smaller file
                    img = img.convert("P", palette=Image.ADAPTIVE, colors=max(2, int(256 * quality / 100)))
                img.save(dst_p, format="PNG", optimize=optimize)

        else:
            #fallback: try saving in current format, else copy
            try:
                img.save(dst_p)
            except Exception:
                shutil.copyfile(src_p, dst_p)

    new_size = dst_p.stat().st_size
    return {"src": str(src_p), "dst": str(dst_p), "orig_size": orig_size, "new_size": new_size}


#small batch helper
from concurrent.futures import ThreadPoolExecutor, as_completed


def compress_batch(paths, out_dir: str, workers: int = 4, **kwargs):
    """Compress multiple image files concurrently and save them to the output directory.

    Args:
        paths (list[str] or list[Path]): List of source image file paths to compress.
        out_dir (str): Directory where compressed images will be saved.
        workers (int, optional): Number of concurrent worker threads. Defaults to 4.
        **kwargs: Additional keyword arguments passed to the `compress` function
            (e.g., quality, max_size, convert_to, optimize, preserve_exif, progressive, webp_lossless).

    Returns:
        list[dict]: List of dictionaries with compression results for each image. Each dictionary contains:
            - "src" (str): Source file path.
            - "dst" (str, optional): Destination file path (if compression succeeded).
            - "orig_size" (int, optional): Original file size in bytes.
            - "new_size" (int, optional): Compressed file size in bytes.
            - "error" (str, optional): Error message if compression failed.

    Example:
        >>> results = compress_batch(["img1.jpg", "img2.png"], "compressed_images", quality=80)
        >>> results
        [
            {'src': 'img1.jpg', 'dst': 'compressed_images/img1.jpg', 'orig_size': 204800, 'new_size': 102400},
            {'src': 'img2.png', 'dst': 'compressed_images/img2.png', 'orig_size': 512000, 'new_size': 256000}
        ]
    """
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {}
        for p in paths:
            p = Path(p)
            dst = out_dir_p / p.name
            futures[ex.submit(compress, str(p), str(dst), **kwargs)] = str(p)
        for fut in as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as e:
                results.append({"src": futures[fut], "error": str(e)})
    return results
