from flask import Flask, render_template, request, jsonify, send_from_directory, session
import os
import json
import re
import uuid
import secrets
import threading
import time
from datetime import datetime, timedelta
import logging
from createAct import (
    generate_band_profile, create_band_backstory, extract_band_members,
    generate_discography_info, generate_dall_e_image, create_project_directory,
    build_band_photo_prompt, create_html_content, save_html_to_file, save_band_info
)
import glob

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store generation status (H-006: protected by lock)
generation_status = {}
generation_lock = threading.Lock()

# Simple rate limiting (H-005): track generation timestamps per IP
_rate_limit = {}
_rate_lock = threading.Lock()
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 3600  # 1 hour

# Path validation pattern
SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')


def cleanup_old_generations():
    """Remove generation status entries older than 1 hour"""
    cutoff = time.time() - 3600
    with generation_lock:
        to_remove = [gid for gid, info in generation_status.items()
                     if info.get('_created', 0) < cutoff]
        for gen_id in to_remove:
            del generation_status[gen_id]


@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/generate')
def generate_page():
    """Band generation page"""
    return render_template('generate.html')


@app.route('/gallery')
def gallery():
    """Gallery of generated bands"""
    bands = []

    for band_dir in glob.glob(os.path.join(app.root_path, "*/home.html")):
        band_name = os.path.basename(os.path.dirname(band_dir))
        info_path = os.path.join(app.root_path, band_name, 'band_info.json')

        # Skip legacy pages that lack a band_info.json metadata file (C-001/C-002)
        if not os.path.exists(info_path):
            continue

        # Skip bands whose directory names can't be routed (N-028)
        if not SAFE_BAND_NAME.match(band_name):
            continue

        # Read display name from metadata, fall back to regex derivation
        try:
            with open(info_path, 'r') as f:
                band_info = json.load(f)
            display_name = band_info.get('display_name', re.sub(r'([A-Z])', r' \1', band_name).strip())
        except (json.JSONDecodeError, OSError):
            display_name = re.sub(r'([A-Z])', r' \1', band_name).strip()

        bands.append({
            'name': display_name,
            'directory': band_name,
            'has_photo': os.path.exists(os.path.join(app.root_path, band_name, 'band_photo.jpg'))
        })

    return render_template('gallery.html', bands=bands)


@app.route('/band/<band_name>/')
def view_band(band_name):
    """View a specific band's page"""
    if not SAFE_BAND_NAME.match(band_name):
        return "Invalid band name", 400
    band_path = os.path.join(band_name, 'home.html')
    if os.path.exists(band_path):
        return send_from_directory(band_name, 'home.html')
    else:
        return "Band not found", 404


@app.route('/band/<band_name>/<filename>')
def band_assets(band_name, filename):
    """Serve band assets like photos"""
    if not SAFE_BAND_NAME.match(band_name):
        return "Invalid band name", 400
    return send_from_directory(band_name, filename)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate a new band"""
    try:
        # CSRF check (H-004): verify Origin/Referer matches our host
        origin = request.headers.get('Origin', '')
        referer = request.headers.get('Referer', '')
        if origin and request.host not in origin:
            return jsonify({'success': False, 'error': 'Invalid request origin.'}), 403
        if not origin and referer and request.host not in referer:
            return jsonify({'success': False, 'error': 'Invalid request origin.'}), 403

        # Rate limiting (H-005)
        client_ip = request.remote_addr
        now = time.time()
        with _rate_lock:
            timestamps = _rate_limit.get(client_ip, [])
            timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
            if len(timestamps) >= RATE_LIMIT_MAX:
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait before generating another band.'
                }), 429
            timestamps.append(now)
            _rate_limit[client_ip] = timestamps

        cleanup_old_generations()

        generation_id = uuid.uuid4().hex[:12]

        # Grab user selections (empty string = let AI decide)
        data = request.get_json(silent=True) or {}
        constraints = {
            'genre1': data.get('genre1', ''),
            'genre2': data.get('genre2', ''),
            'nationality': data.get('nationality', ''),
            'style_name': data.get('style_name', ''),
            'era': data.get('era', ''),
        }

        with generation_lock:
            generation_status[generation_id] = {
                'status': 'starting',
                'progress': 0,
                'message': 'Initializing band generation...',
                'band_name': None,
                'directory': None,
                '_created': time.time()
            }

        thread = threading.Thread(target=generate_band_async, args=(generation_id, constraints))
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'generation_id': generation_id,
            'message': 'Band generation started'
        })

    except Exception as e:
        logger.error(f"Error starting band generation: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while starting band generation. Please try again.'
        }), 500


@app.route('/api/status/<generation_id>')
def api_status(generation_id):
    """Check the status of a band generation"""
    with generation_lock:
        status = generation_status.get(generation_id, {
            'status': 'not_found',
            'progress': 0,
            'message': 'Generation not found'
        })
        # Don't expose internal fields to the client
        return jsonify({k: v for k, v in status.items() if not k.startswith('_')})


def _update_status(generation_id, updates):
    """Thread-safe update of generation status."""
    with generation_lock:
        if generation_id in generation_status:
            generation_status[generation_id].update(updates)


def generate_band_async(generation_id, constraints=None):
    """Generate a band asynchronously"""
    try:
        _update_status(generation_id, {
            'status': 'generating_profile',
            'progress': 10,
            'message': 'Creating band profile...'
        })

        band_profile = generate_band_profile(constraints=constraints)

        _update_status(generation_id, {
            'status': 'creating_directory',
            'progress': 20,
            'message': f'Setting up {band_profile["Band Name"]}...',
            'band_name': band_profile['Band Name']
        })

        output_dir = create_project_directory(band_profile['Band Name'])
        _update_status(generation_id, {'directory': output_dir})

        _update_status(generation_id, {
            'status': 'generating_backstory',
            'progress': 35,
            'message': 'Writing band backstory...'
        })

        backstory = create_band_backstory(band_profile)

        _update_status(generation_id, {
            'status': 'extracting_members',
            'progress': 50,
            'message': 'Identifying band members...'
        })

        band_members = extract_band_members(band_profile, backstory)

        _update_status(generation_id, {
            'status': 'generating_discography',
            'progress': 60,
            'message': 'Creating discography...'
        })

        albums = generate_discography_info(band_profile, backstory)

        _update_status(generation_id, {
            'status': 'generating_photo',
            'progress': 75,
            'message': 'Taking band photo...'
        })

        # Build era-appropriate DALL-E prompt
        photo_prompt = build_band_photo_prompt(band_profile, band_members)
        generate_dall_e_image(photo_prompt, os.path.join(output_dir, 'band_photo.jpg'))

        _update_status(generation_id, {
            'status': 'creating_page',
            'progress': 90,
            'message': 'Building fan page...'
        })

        html_content = create_html_content(band_profile, backstory, albums, band_members, output_dir)
        save_html_to_file(html_content, output_dir)
        save_band_info(band_profile, output_dir)

        _update_status(generation_id, {
            'status': 'complete',
            'progress': 100,
            'message': f'{band_profile["Band Name"]} is ready to rock!'
        })

    except Exception as e:
        logger.error(f"Error in band generation {generation_id}: {e}", exc_info=True)
        _update_status(generation_id, {
            'status': 'error',
            'progress': 0,
            'message': 'An error occurred during band generation. Please try again.'
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
