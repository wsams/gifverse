#!/usr/bin/env python3
"""
GIFverse CLI - Command line tool for creating seamless GIF loops
"""

import argparse
import os
import sys
from pathlib import Path
from gif_processor import process_gif, validate_gif_file

def process_gif_cli(input_path, output_path):
    """
    Process GIF to create seamless loop by concatenating original with reversed frames
    """
    try:
        # Use the shared processor with verbose output
        process_gif(input_path, output_path, verbose=True)
        return True

    except Exception as e:
        print(f"Error processing GIF: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Create seamless GIF loops by concatenating original with reversed frames')
    parser.add_argument('input', help='Input GIF file path')
    parser.add_argument('-o', '--output', help='Output GIF file path (default: input_seamless.gif)')
    parser.add_argument('--version', action='version', version='GIFverse CLI 1.0')

    args = parser.parse_args()

    # Validate input file
    try:
        validate_gif_file(args.input)
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Generate output filename if not provided
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_seamless{input_path.suffix}"

    # Process the GIF
    success = process_gif_cli(args.input, output_path)

    if success:
        print(f"Done! Seamless GIF saved to: {output_path}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
