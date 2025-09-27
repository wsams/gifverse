#!/usr/bin/env python3
"""
Unit tests for gif_processor module
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image, ImageDraw, ImageSequence
import sys

# Add parent directory to path to import gif_processor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gif_processor import process_gif, validate_gif_file


class TestGifProcessor(unittest.TestCase):
    """Test cases for gif_processor module"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_gif_path = os.path.join(self.temp_dir, "test.gif")
        self.output_gif_path = os.path.join(self.temp_dir, "output.gif")

        # Create a simple test GIF
        self.create_test_gif()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_test_gif(self, frames=5):
        """Create a simple test GIF with specified number of frames"""
        images = []
        durations = []

        for i in range(frames):
            # Create a 100x100 image with a moving circle
            img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)

            # Draw a circle that moves across the frame
            x = 20 + (i * 15)
            y = 50
            radius = 10

            draw.ellipse([x-radius, y-radius, x+radius, y+radius],
                        fill=(255, 0, 0, 255), outline=(0, 0, 0, 255))

            images.append(img)
            durations.append(100)  # 100ms per frame

        # Save as GIF
        images[0].save(
            self.test_gif_path,
            save_all=True,
            append_images=images[1:],
            duration=durations,
            loop=0,
            optimize=True
        )

    def test_validate_gif_file_success(self):
        """Test validate_gif_file with valid GIF file"""
        result = validate_gif_file(self.test_gif_path)
        self.assertTrue(result)  # Should return True for valid GIF

    def test_validate_gif_file_nonexistent(self):
        """Test validate_gif_file with non-existent file"""
        with self.assertRaises(ValueError) as context:
            validate_gif_file("nonexistent.gif")
        self.assertIn("does not exist", str(context.exception))

    def test_validate_gif_file_not_gif(self):
        """Test validate_gif_file with non-GIF file"""
        # Create a text file
        text_file = os.path.join(self.temp_dir, "test.txt")
        with open(text_file, 'w') as f:
            f.write("not a gif")

        with self.assertRaises(ValueError) as context:
            validate_gif_file(text_file)
        self.assertIn("Invalid GIF file", str(context.exception))

    def test_validate_gif_file_too_small(self):
        """Test validate_gif_file with file that's too small"""
        # Create a very small file
        small_file = os.path.join(self.temp_dir, "small.gif")
        with open(small_file, 'wb') as f:
            f.write(b"GIF89a")  # Just GIF header

        with self.assertRaises(ValueError) as context:
            validate_gif_file(small_file)
        self.assertIn("Invalid GIF file", str(context.exception))

    def test_validate_gif_file_too_large(self):
        """Test validate_gif_file with file that's too large"""
        with self.assertRaises(ValueError) as context:
            validate_gif_file(self.test_gif_path, max_size=100)  # 100 bytes limit
        self.assertIn("too large", str(context.exception))

    def test_validate_gif_file_insufficient_frames(self):
        """Test validate_gif_file with GIF that has too few frames"""
        # Create a single-frame GIF
        single_frame_gif = os.path.join(self.temp_dir, "single.gif")
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
        img.save(single_frame_gif, format='GIF')

        # Single frame GIFs should pass validation (they're valid GIFs)
        result = validate_gif_file(single_frame_gif)
        self.assertTrue(result)

    def test_process_gif_success(self):
        """Test process_gif with valid input"""
        result = process_gif(self.test_gif_path, self.output_gif_path)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_gif_path))
        self.assertEqual(result, self.output_gif_path)

        # Check that output file is a valid GIF
        with Image.open(self.output_gif_path) as img:
            self.assertEqual(img.format, 'GIF')
            # Should have double the frames minus 1 (original + reversed, but last frame of original = first frame of reversed)
            frame_count = sum(1 for _ in ImageSequence.Iterator(img))
            self.assertEqual(frame_count, 9)  # 5 original + 4 reversed (last frame of original = first frame of reversed)

    def test_process_gif_verbose_output(self):
        """Test process_gif with verbose output"""
        with patch('builtins.print') as mock_print:
            result = process_gif(self.test_gif_path, self.output_gif_path, verbose=True)

            # Check that verbose messages were printed
            self.assertTrue(mock_print.called)
            self.assertTrue(os.path.exists(self.output_gif_path))

    def test_process_gif_invalid_input(self):
        """Test process_gif with invalid input file"""
        with self.assertRaises(FileNotFoundError):
            process_gif("nonexistent.gif", self.output_gif_path)

    def test_process_gif_insufficient_frames(self):
        """Test process_gif with GIF that has too few frames"""
        # Create a single-frame GIF
        single_frame_gif = os.path.join(self.temp_dir, "single.gif")
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
        img.save(single_frame_gif, format='GIF')

        with self.assertRaises(ValueError) as context:
            process_gif(single_frame_gif, self.output_gif_path)
        self.assertIn("at least 2 frames", str(context.exception))

    def test_process_gif_preserves_durations(self):
        """Test that process_gif preserves frame durations"""
        result = process_gif(self.test_gif_path, self.output_gif_path)

        with Image.open(self.output_gif_path) as img:
            frames = list(ImageSequence.Iterator(img))

            # Check that durations are preserved
            for i, frame in enumerate(frames):
                duration = frame.info.get('duration', 0)
                self.assertEqual(duration, 100)  # Should match original duration

    def test_process_gif_creates_seamless_loop(self):
        """Test that process_gif creates a seamless loop"""
        result = process_gif(self.test_gif_path, self.output_gif_path)

        with Image.open(self.output_gif_path) as img:
            frames = list(ImageSequence.Iterator(img))

            # First frame should match last frame (for seamless loop)
            first_frame = frames[0]
            last_frame = frames[-1]

            # Convert to RGB for comparison (ignore alpha channel)
            first_rgb = first_frame.convert('RGB')
            last_rgb = last_frame.convert('RGB')

            # They should be identical
            self.assertEqual(first_rgb.tobytes(), last_rgb.tobytes())

    def test_process_gif_handles_rgba_conversion(self):
        """Test that process_gif handles RGBA conversion properly"""
        # Create a GIF with different color modes
        result = process_gif(self.test_gif_path, self.output_gif_path)

        with Image.open(self.output_gif_path) as img:
            frames = list(ImageSequence.Iterator(img))

            # All frames should be in RGB mode (GIFs are typically RGB)
            for frame in frames:
                self.assertEqual(frame.mode, 'RGB')

    def test_process_gif_error_handling(self):
        """Test process_gif error handling"""
        # Test with corrupted file
        corrupted_file = os.path.join(self.temp_dir, "corrupted.gif")
        with open(corrupted_file, 'wb') as f:
            f.write(b"not a valid gif file")

        with self.assertRaises(Exception):
            process_gif(corrupted_file, self.output_gif_path)

    def test_process_gif_output_directory_creation(self):
        """Test that process_gif creates output directory if needed"""
        output_dir = os.path.join(self.temp_dir, "nested", "output.gif")

        # Create the directory first
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        result = process_gif(self.test_gif_path, output_dir)

        self.assertTrue(os.path.exists(output_dir))
        self.assertEqual(result, output_dir)

    def test_process_gif_overwrites_existing_file(self):
        """Test that process_gif overwrites existing output file"""
        # Create an existing file
        with open(self.output_gif_path, 'w') as f:
            f.write("existing content")

        result = process_gif(self.test_gif_path, self.output_gif_path)

        # Should overwrite the existing file
        self.assertTrue(os.path.exists(self.output_gif_path))
        self.assertNotEqual(os.path.getsize(self.output_gif_path), 0)


class TestGifProcessorIntegration(unittest.TestCase):
    """Integration tests for gif_processor module"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_workflow(self):
        """Test the complete workflow from validation to processing"""
        # Create test GIF
        test_gif = os.path.join(self.temp_dir, "test.gif")
        output_gif = os.path.join(self.temp_dir, "output.gif")

        # Create a simple test GIF
        images = []
        for i in range(3):
            img = Image.new('RGBA', (50, 50), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.ellipse([10+i*10, 10, 20+i*10, 20], fill=(255, 0, 0, 255))
            images.append(img)

        images[0].save(test_gif, save_all=True, append_images=images[1:],
                      duration=[100, 100, 100], loop=0)

        # Validate
        validate_gif_file(test_gif)

        # Process
        result = process_gif(test_gif, output_gif, verbose=True)

        # Verify
        self.assertTrue(os.path.exists(output_gif))
        self.assertEqual(result, output_gif)

        with Image.open(output_gif) as img:
            frame_count = sum(1 for _ in ImageSequence.Iterator(img))
            self.assertEqual(frame_count, 5)  # 3 original + 2 reversed (last frame of original = first frame of reversed)


if __name__ == '__main__':
    unittest.main()
