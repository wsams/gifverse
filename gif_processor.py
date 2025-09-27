#!/usr/bin/env python3
"""
GIF Processor - Core module for creating seamless GIF loops
by concatenating original GIF frames with their reversed version.
"""

import os
from PIL import Image, ImageSequence


def process_gif(input_path, output_path, verbose=False):
    """
    Process GIF to create seamless loop by concatenating original with reversed frames

    Args:
        input_path (str): Path to input GIF file
        output_path (str): Path where output GIF will be saved
        verbose (bool): Whether to print progress messages

    Returns:
        str: Path to the created output file on success

    Raises:
        ValueError: If the file is not a GIF or has insufficient frames
        Exception: For other processing errors
    """
    try:
        # Open the GIF
        with Image.open(input_path) as img:
            # Check if it's actually a GIF
            if img.format != 'GIF':
                raise ValueError("File is not a GIF")

            # Extract all frames
            frames = []
            durations = []

            for frame in ImageSequence.Iterator(img):
                # Convert to RGBA to ensure compatibility
                frame = frame.convert('RGBA')
                frames.append(frame.copy())

                # Get frame duration (default to 100ms if not specified)
                duration = frame.info.get('duration', 100)
                durations.append(duration)

            if len(frames) < 2:
                raise ValueError("GIF must have at least 2 frames")

            if verbose:
                print(f"Processing GIF with {len(frames)} frames...")

            # Create reversed frames (excluding the first frame to avoid duplication)
            reversed_frames = frames[:-1][::-1]  # Reverse all but last frame
            reversed_durations = durations[:-1][::-1]  # Reverse durations too

            # Combine original and reversed frames
            combined_frames = frames + reversed_frames
            combined_durations = durations + reversed_durations

            if verbose:
                print(f"Creating seamless loop with {len(combined_frames)} total frames...")

            # Save as GIF with proper optimization
            combined_frames[0].save(
                output_path,
                save_all=True,
                append_images=combined_frames[1:],
                duration=combined_durations,
                loop=0,  # Infinite loop
                optimize=True,
                disposal=2  # Restore to background
            )

            if verbose:
                print(f"Successfully created seamless GIF: {output_path}")

            return output_path

    except Exception as e:
        if verbose:
            print(f"Error processing GIF: {str(e)}")
        raise


def validate_gif_file(file_path, max_size=None):
    """
    Validate that a file is a valid GIF and optionally check size

    Args:
        file_path (str): Path to the file to validate
        max_size (int, optional): Maximum file size in bytes

    Returns:
        bool: True if valid

    Raises:
        ValueError: If file is invalid or too large
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File does not exist: {file_path}")

    # Check file size if specified
    if max_size:
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")

    # Check if it's actually a GIF
    try:
        with Image.open(file_path) as img:
            if img.format != 'GIF':
                raise ValueError("File is not a GIF")
    except Exception as e:
        raise ValueError(f"Invalid GIF file: {str(e)}")

    return True
