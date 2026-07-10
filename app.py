from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import os
import re
import threading
import uuid
from datetime import datetime, timedelta
import logging
from createAct import (
    generate_band_profile, create_band_backstory, extract_band_members,
    generate_discography_info, generate_dall_e_image, create_project_directory,
    build_band_photo_prompt, create_html_content, save_html_to_file
)
import glob

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path-traversal defense: only allow safe band-name characters in URL path params.
SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')

# Store generation status (lazily pruned in api_generate). Written by worker
# threads and read by request threads, so every access takes STATUS_LOCK.
generation_status = {}
STATUS_LOCK = threading.Lock()

# A generation that has reached one of these is finished and safe to prune.
TERMINAL_STATUSES = frozenset({'complete', 'error'})

# Fields api_status is allowed to echo back; anything else (created_at) is internal.
PUBLIC_STATUS_FIELDS = ('status', 'progress', 'message', 'band_name', 'directory')


def cleanup_old_generations(max_age_minutes=60):
    """Remove *finished* generation_status entries older than max_age_minutes.

    Lazily called from api_generate so we don't need a background thread.

    Only terminal entries are pruned. A generation that is still running keeps
    its entry however old it is: dropping it would strand the worker thread and
    leave the browser polling an id that never resolves.
    """
    cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
    with STATUS_LOCK:
        stale = [
            key for key, entry in generation_status.items()
            if entry.get('status') in TERMINAL_STATUSES
            and entry.get('created_at', datetime.max) < cutoff
        ]
        for key in stale:
            generation_status.pop(key, None)
    if stale:
        logger.info(f"Cleaned up {len(stale)} stale generation status entries")


def update_status(generation_id, **fields):
    """Merge fields into a generation's status entry if it still exists.

    Returns False when the entry is gone. Callers must never index
    generation_status directly: generate_band_async's error handler runs on
    exactly the path where the entry may be absent, and a KeyError raised there
    would kill the worker thread with no status ever written.
    """
    with STATUS_LOCK:
        entry = generation_status.get(generation_id)
        if entry is None:
            logger.warning("Status entry %s is gone; dropping update", generation_id)
            return False
        entry.update(fields)
        return True


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

    for band_dir in glob.glob("*/home.html"):
        band_name = os.path.dirname(band_dir)
        # Directories outside SAFE_BAND_NAME can never be served by view_band,
        # so listing them here would render a dead link and a broken image.
        if not SAFE_BAND_NAME.match(band_name):
            logging.warning("Skipping unservable band directory: %s", band_name)
            continue
        display_name = re.sub(r'([A-Z])', r' \1', band_name).strip()
        bands.append({
            'name': display_name,
            'directory': band_name,
            'has_photo': os.path.exists(os.path.join(band_name, 'band_photo.jpg'))
        })

    return render_template('gallery.html', bands=bands)


@app.route('/band/<band_name>/')
def view_band(band_name):
    """View a specific band's page"""
    if not SAFE_BAND_NAME.match(band_name):
        abort(404)
    band_path = os.path.join(band_name, 'home.html')
    if os.path.exists(band_path):
        return send_from_directory(band_name, 'home.html')
    else:
        return "Band not found", 404


@app.route('/band/<band_name>/<filename>')
def band_assets(band_name, filename):
    """Serve band assets like photos"""
    if not SAFE_BAND_NAME.match(band_name):
        abort(404)
    return send_from_directory(band_name, filename)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate a new band"""
    try:
        # Lazy cleanup so generation_status doesn't grow unboundedly.
        cleanup_old_generations()

        # uuid, not a second-resolution timestamp: two POSTs landing in the same
        # second would otherwise share one id, one status dict and one output dir.
        generation_id = uuid.uuid4().hex

        with STATUS_LOCK:
            generation_status[generation_id] = {
                'status': 'starting',
                'progress': 0,
                'message': 'Initializing band generation...',
                'band_name': None,
                'directory': None,
                'created_at': datetime.now()
            }

        thread = threading.Thread(target=generate_band_async, args=(generation_id,))
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
            'error': str(e)
        }), 500


@app.route('/api/status/<generation_id>')
def api_status(generation_id):
    """Check the status of a band generation"""
    with STATUS_LOCK:
        entry = generation_status.get(generation_id)
        status = {k: entry[k] for k in PUBLIC_STATUS_FIELDS if k in entry} if entry else None

    if status is None:
        status = {
            'status': 'not_found',
            'progress': 0,
            'message': 'Generation not found'
        }
    return jsonify(status)


def generate_band_async(generation_id):
    """Generate a band asynchronously"""
    try:
        update_status(
            generation_id,
            status='generating_profile',
            progress=10,
            message='Creating band profile...'
        )

        band_profile = generate_band_profile()

        update_status(
            generation_id,
            status='creating_directory',
            progress=20,
            message=f'Setting up {band_profile["Band Name"]}...',
            band_name=band_profile['Band Name']
        )

        output_dir = create_project_directory(band_profile['Band Name'])
        update_status(generation_id, directory=output_dir)

        update_status(
            generation_id,
            status='generating_backstory',
            progress=35,
            message='Writing band backstory...'
        )

        backstory = create_band_backstory(band_profile)

        update_status(
            generation_id,
            status='extracting_members',
            progress=50,
            message='Identifying band members...'
        )

        band_members = extract_band_members(band_profile, backstory)

        update_status(
            generation_id,
            status='generating_discography',
            progress=60,
            message='Creating discography...'
        )

        albums = generate_discography_info(band_profile, backstory)

        update_status(
            generation_id,
            status='generating_photo',
            progress=75,
            message='Taking band photo...'
        )

        # Build era-appropriate DALL-E prompt
        photo_prompt = build_band_photo_prompt(band_profile, band_members)
        generate_dall_e_image(photo_prompt, os.path.join(output_dir, 'band_photo.jpg'))

        update_status(
            generation_id,
            status='creating_page',
            progress=90,
            message='Building fan page...'
        )

        html_content = create_html_content(band_profile, backstory, albums, band_members, output_dir)
        save_html_to_file(html_content, output_dir)

        update_status(
            generation_id,
            status='complete',
            progress=100,
            message=f'{band_profile["Band Name"]} is ready to rock!'
        )

    except Exception as e:
        logger.exception("Error in band generation %s", generation_id)
        update_status(
            generation_id,
            status='error',
            progress=0,
            message=f'Error: {str(e)}'
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
