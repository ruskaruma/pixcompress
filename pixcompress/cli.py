import click
from pathlib import Path
from .core import compress, compress_batch

@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('--quality', '-q', default=85, type=int, help='Quality 0-100')
@click.option('--max-width', default=0, type=int, help='Max width in pixels')
@click.option('--max-height', default=0, type=int, help='Max height in pixels')
@click.option('--output', '-o', type=click.Path(), help='Output filename')
def cli(input_file, quality, max_width, max_height, output):
    """Compress images while keeping originals intact."""
    input_path = Path(input_file)
    if not output:
        stem=input_path.stem
        suffix=input_path.suffix
        output=input_path.parent / f"{stem}_compressed{suffix}"
    max_size = None
    if max_width>0 or max_height > 0:
        max_size=(max_width or 0, max_height or 0)
    
    try:
        result=compress(str(input_path), str(output), quality=quality, max_size=max_size)
        original_size=result['orig_size']
        compressed_size=result['new_size']
        ratio=(1-compressed_size / original_size) * 100
        click.echo(f"Compressed: {input_path.name}")
        click.echo(f"Output: {output}")
        click.echo(f"Size: {original_size:,} -> {compressed_size:,} bytes ({ratio:.1f}% reduction)")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
