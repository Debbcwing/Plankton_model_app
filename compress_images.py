#!/usr/bin/env python3
"""
Image compression script to convert PNG to WebP format
Reduces file size by 70-80% with minimal quality loss
"""

from PIL import Image
import os
from pathlib import Path

def compress_to_webp(input_path, output_path=None, quality=80):
    """
    Convert PNG to WebP format

    Args:
        input_path: Path to input PNG file
        output_path: Path to output WebP file (optional)
        quality: WebP quality (0-100, default 80)
    """
    if output_path is None:
        output_path = input_path.replace('.png', '.webp')

    # Open and convert image
    img = Image.open(input_path)

    # Convert RGBA to RGB if necessary
    if img.mode == 'RGBA':
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        img = background

    # Save as WebP
    img.save(output_path, 'WebP', quality=quality, method=6)

    # Get file sizes
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    reduction = (1 - compressed_size / original_size) * 100

    print(f"✓ {os.path.basename(input_path)}")
    print(f"  {original_size / 1024 / 1024:.2f} MB → {compressed_size / 1024 / 1024:.2f} MB")
    print(f"  Reduction: {reduction:.1f}%\n")

    return output_path

def main():
    print("=" * 60)
    print("Image Compression Script - PNG to WebP")
    print("=" * 60)
    print()

    # Find all PNG files in Planktoomics folder
    planktoomics_dir = Path("Planktoomics")

    if not planktoomics_dir.exists():
        print("❌ Planktoomics folder not found!")
        print("Looking for PNGs in current directory...")
        png_files = list(Path(".").glob("*.png"))
    else:
        png_files = list(planktoomics_dir.glob("*.png"))

    if not png_files:
        print("❌ No PNG files found!")
        return

    print(f"Found {len(png_files)} PNG files to compress:\n")

    total_original = 0
    total_compressed = 0

    for png_file in png_files:
        try:
            original_size = os.path.getsize(png_file)
            total_original += original_size

            webp_file = str(png_file).replace('.png', '.webp')
            compress_to_webp(str(png_file), webp_file, quality=80)

            compressed_size = os.path.getsize(webp_file)
            total_compressed += compressed_size

        except Exception as e:
            print(f"❌ Error processing {png_file}: {e}\n")

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total original size: {total_original / 1024 / 1024:.2f} MB")
    print(f"Total compressed size: {total_compressed / 1024 / 1024:.2f} MB")
    print(f"Total reduction: {(1 - total_compressed / total_original) * 100:.1f}%")
    print()
    print("✅ Compression complete!")
    print()
    print("Next steps:")
    print("1. Update app.py to use .webp files instead of .png")
    print("2. Test the app to ensure images load correctly")
    print("3. (Optional) Delete original .png files to save space")

if __name__ == "__main__":
    main()
