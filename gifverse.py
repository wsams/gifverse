#!/usr/bin/env python3
"""
GIFverse - A Python web application that creates seamless GIF loops
by concatenating original GIF frames with their reversed version.
"""

import os
import hashlib
import time
import tempfile
import shutil
from urllib.parse import urlparse
from pathlib import Path
import math

import requests
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from PIL import Image, ImageSequence
import io
from gif_processor import process_gif, validate_gif_file

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Template filters
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """Convert timestamp to readable date format"""
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# Configuration
UPLOAD_FOLDER = 'tmp'
OUTPUT_FOLDER = 'gifverses'
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_gif_from_url(url):
    """Download GIF from URL and return file path"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Check if it's actually a GIF
        if not response.headers.get('content-type', '').startswith('image/gif'):
            raise ValueError("URL does not point to a GIF image")

        # Create temporary file
        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith('.gif'):
            filename += '.gif'

        tmp_path = os.path.join(UPLOAD_FOLDER, f"temp_{int(time.time())}_{filename}")
        with open(tmp_path, 'wb') as f:
            f.write(response.content)

        return tmp_path, filename
    except Exception as e:
        raise ValueError(f"Failed to download GIF: {str(e)}")

def process_gif_web(input_path, output_filename):
    """
    Process GIF to create seamless loop by concatenating original with reversed frames
    """
    try:
        # Create output path
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Use the shared processor
        return process_gif(input_path, output_path, verbose=False)

    except Exception as e:
        raise ValueError(f"Failed to process GIF: {str(e)}")

@app.route('/')
def index():
    """Main page with upload form"""
    gif_url = request.args.get('gif')
    gifverse_img = ""

    if gif_url and os.path.exists(os.path.join(OUTPUT_FOLDER, gif_url)):
        gifverse_img = f'<img src="gifverses/{gif_url}" alt="gifverse" class="img-responsive" />'

    return render_template('index.html', gifverse_img=gifverse_img)

@app.route('/process', methods=['POST'])
def process_gif_upload():
    """Process uploaded GIF or URL"""
    try:
        # Check if URL is provided and not empty
        url_input = request.form.get('url', '').strip()
        file_input = request.files.get('gif')

        # Handle URL input - only if it's a valid URL
        if url_input and len(url_input) > 5 and (url_input.startswith(('http://', 'https://')) or '.' in url_input):
            if not url_input.startswith(('http://', 'https://')):
                url_input = 'http://' + url_input

            input_path, filename = download_gif_from_url(url_input)
            cleanup_input = True
        # Handle file upload
        elif file_input and file_input.filename:
            if not file_input.filename.lower().endswith('.gif'):
                flash('Please upload a GIF file')
                return redirect(url_for('index'))

            # Save uploaded file
            filename = file_input.filename
            input_path = os.path.join(UPLOAD_FOLDER, f"upload_{int(time.time())}_{filename}")
            file_input.save(input_path)
            cleanup_input = True
        else:
            flash('Please provide either a GIF file or a URL')
            return redirect(url_for('index'))

        # Validate the GIF file
        try:
            validate_gif_file(input_path, max_size=MAX_FILE_SIZE)
        except ValueError as e:
            flash(f'Error: {str(e)}')
            if cleanup_input:
                os.unlink(input_path)
            return redirect(url_for('index'))

        # Generate output filename
        timestamp = int(time.time())
        output_filename = f"gifverse_{timestamp}_{filename}"

        # Process the GIF
        output_path = process_gif_web(input_path, output_filename)

        # Cleanup input file
        if cleanup_input:
            os.unlink(input_path)

        # Redirect to show result
        return redirect(url_for('index', gif=output_filename))

    except Exception as e:
        flash(f'Error: {str(e)}')
        if 'input_path' in locals() and cleanup_input and os.path.exists(input_path):
            os.unlink(input_path)
        return redirect(url_for('index'))

@app.route('/gifverses/<filename>')
def serve_gif(filename):
    """Serve processed GIF files"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/gallery')
def gallery():
    """Gallery page showing all processed GIFs with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of GIFs per page

    # Get all GIF files from the output directory
    gif_files = []
    if os.path.exists(OUTPUT_FOLDER):
        for filename in os.listdir(OUTPUT_FOLDER):
            if filename.lower().endswith('.gif'):
                file_path = os.path.join(OUTPUT_FOLDER, filename)
                file_stat = os.stat(file_path)
                gif_files.append({
                    'filename': filename,
                    'size': file_stat.st_size,
                    'created': file_stat.st_mtime,
                    'url': url_for('serve_gif', filename=filename)
                })

    # Sort by creation time (newest first)
    gif_files.sort(key=lambda x: x['created'], reverse=True)

    # Calculate pagination
    total_gifs = len(gif_files)
    total_pages = math.ceil(total_gifs / per_page) if total_gifs > 0 else 1

    # Validate page number
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # Get GIFs for current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    gifs_on_page = gif_files[start_idx:end_idx]

    # Calculate pagination info
    has_prev = page > 1
    has_next = page < total_pages

    # Generate page numbers for pagination
    page_numbers = []
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    for p in range(start_page, end_page + 1):
        page_numbers.append(p)

    return render_template('gallery.html',
                         gifs=gifs_on_page,
                         page=page,
                         total_pages=total_pages,
                         total_gifs=total_gifs,
                         has_prev=has_prev,
                         has_next=has_next,
                         page_numbers=page_numbers,
                         per_page=per_page)

if __name__ == '__main__':
    # Get port from environment variable (for containerized deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    app.run(debug=debug, host='0.0.0.0', port=port)
