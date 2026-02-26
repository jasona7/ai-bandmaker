from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import threading
from datetime import datetime
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

# Store generation status
generation_status = {}


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
        import re
        display_name = re.sub(r'([A-Z])', r' \1', band_name).strip()
        bands.append({
            'name': display_name,
            'directory': band_name,
            'has_photo': os.path.exists(os.path.join(band_name, 'band_photo.jpg'))
        })

    return render_template('gallery.html', bands=bands)


@app.route('/band/<band_name>')
def view_band(band_name):
    """View a specific band's page"""
    band_path = os.path.join(band_name, 'home.html')
    if os.path.exists(band_path):
        return send_from_directory(band_name, 'home.html')
    else:
        return "Band not found", 404


@app.route('/band/<band_name>/<filename>')
def band_assets(band_name, filename):
    """Serve band assets like photos"""
    return send_from_directory(band_name, filename)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate a new band"""
    try:
        generation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        generation_status[generation_id] = {
            'status': 'starting',
            'progress': 0,
            'message': 'Initializing band generation...',
            'band_name': None,
            'directory': None
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
    status = generation_status.get(generation_id, {
        'status': 'not_found',
        'progress': 0,
        'message': 'Generation not found'
    })
    return jsonify(status)


def generate_band_async(generation_id):
    """Generate a band asynchronously"""
    try:
        generation_status[generation_id].update({
            'status': 'generating_profile',
            'progress': 10,
            'message': 'Creating band profile...'
        })

        band_profile = generate_band_profile()

        generation_status[generation_id].update({
            'status': 'creating_directory',
            'progress': 20,
            'message': f'Setting up {band_profile["Band Name"]}...',
            'band_name': band_profile['Band Name']
        })

        output_dir = create_project_directory(band_profile['Band Name'])
        generation_status[generation_id]['directory'] = output_dir

        generation_status[generation_id].update({
            'status': 'generating_backstory',
            'progress': 35,
            'message': 'Writing band backstory...'
        })

        backstory = create_band_backstory(band_profile)

        generation_status[generation_id].update({
            'status': 'extracting_members',
            'progress': 50,
            'message': 'Identifying band members...'
        })

        band_members = extract_band_members(band_profile, backstory)

        generation_status[generation_id].update({
            'status': 'generating_discography',
            'progress': 60,
            'message': 'Creating discography...'
        })

        albums = generate_discography_info(band_profile, backstory)

        generation_status[generation_id].update({
            'status': 'generating_photo',
            'progress': 75,
            'message': 'Taking band photo...'
        })

        # Build era-appropriate DALL-E prompt
        photo_prompt = build_band_photo_prompt(band_profile, band_members)
        generate_dall_e_image(photo_prompt, os.path.join(output_dir, 'band_photo.jpg'))

        generation_status[generation_id].update({
            'status': 'creating_page',
            'progress': 90,
            'message': 'Building fan page...'
        })

        html_content = create_html_content(band_profile, backstory, albums, band_members, output_dir)
        save_html_to_file(html_content, output_dir)

        generation_status[generation_id].update({
            'status': 'complete',
            'progress': 100,
            'message': f'{band_profile["Band Name"]} is ready to rock!'
        })

    except Exception as e:
        logger.error(f"Error in band generation: {e}")
        generation_status[generation_id].update({
            'status': 'error',
            'progress': 0,
            'message': f'Error: {str(e)}'
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
