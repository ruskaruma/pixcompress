from pathlib import Path
from PIL import Image
import shutil
from typing import Union, Optional

def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def _get_exif(img: Image.Image):
    return img.info.get("exif", None)

def _resize_if_needed(img: Image.Image, max_size):
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
    """
    Compress a single image file.
    Returns dict with src, dst, orig_size, new_size
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
