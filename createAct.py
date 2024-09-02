import os
import random
import requests
import logging
from datetime import datetime
import re

# Initialize Faker
from faker import Faker
fake = Faker()

# Get the current year
current_year = datetime.now().year

# Setup logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'execution.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Script execution started.")

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key is set correctly
if not OPENAI_API_KEY:
    logging.error("OpenAI API key is not set.")
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Predefined lists for additional randomization in API prompts
author_styles = [
    "Lester Bangs", "Greil Marcus", "Robert Christgau", "Ellen Willis", 
    "Jon Pareles", "Ben Ratliff", "Paul Morley", "David Fricke", 
    "Ann Powers", "Hunter S. Thompson", "Nick Kent", "Neil Strauss", 
    "Alex Ross", "Chuck Klosterman", "Simon Reynolds", "David Hepworth",
    "Barney Hoskyns", "Cameron Crowe", "Steve Huey", "Jim DeRogatis"
]

genres = [
    "Blues", "Jazz", "Rock", "Folk", "Hip Hop", "Classical", 
    "Electronic", "Pop", "Country", "Reggae", "Punk", "Metal", 
    "Soul", "Funk", "R&B", "Disco", "Gospel", "Latin", "World Music",
    "Ska", "Indie", "Alternative", "Grunge", "Techno", "House",
    "Trance", "Ambient", "Dance", "Dubstep", "Bluegrass", "Opera",
    "Swing", "Bossa Nova", "Afrobeat", "K-Pop", "J-Pop", "Flamenco",
    "Salsa", "Merengue", "Tango", "Zydeco", "Celtic", "New Age",
    "Industrial", "Gothic", "Baroque", "Choral"
]

style_descriptors = [
    "Edgy", "Political", "Party-Band", "Experimental", 
    "Mellow", "Psychedelic", "Minimalist", "Aggressive", 
    "Virtuosic", "Melancholic", "Uplifting", "Retro", 
    "Avant-Garde", "Theatrical", "Romantic", "Rebellious", 
    "Acoustic", "Electronic", "Fusion", "Roots"
]

# Function to generate a random band profile using ChatGPT API
def generate_band_profile():
    prompt = (
        f"Generate a creative band profile including the following details: "
        f"a unique band name, an author style inspired by a music critic, "
        f"a nationality, two distinct music genres, "
        f"a style descriptor, and a reference year between 1955 and 2020. "
        f"The band profile should be formatted in the following format:\n\n"
        f"Band Name: [Band Name]\n"
        f"Author Style: [Author Style]\n"
        f"Nationality: [Nationality]\n"
        f"Genre 1: [Genre 1]\n"
        f"Genre 2: [Genre 2]\n"
        f"Style Name: [Style Name]\n"
        f"Reference Year: [Reference Year]"
    )

    response = generate_chatgpt_response(prompt)

    # Log the raw response for debugging
    logging.info(f"Raw band profile response: {response}")

    try:
        # Use regex to extract information
        band_name = re.search(r"Band Name:\s*(.*)", response).group(1).strip()
        author_style = re.search(r"Author Style:\s*(.*)", response).group(1).strip()
        nationality = re.search(r"Nationality:\s*(.*)", response).group(1).strip()
        genre1 = re.search(r"Genre 1:\s*(.*)", response).group(1).strip()
        genre2 = re.search(r"Genre 2:\s*(.*)", response).group(1).strip()
        style_name = re.search(r"Style Name:\s*(.*)", response).group(1).strip()

        # Extracting and cleaning the reference year
        reference_year_str = re.search(r"Reference Year:\s*([^\n]*)", response).group(1).strip()
        reference_year = int(re.sub(r"[^\d]", "", reference_year_str))  # Remove non-digit characters

        profile = {
            "Band Name": band_name,
            "Author Style": author_style,
            "Nationality": nationality,
            "Genre 1": genre1,
            "Genre 2": genre2,
            "Style Name": style_name,
            "Reference Year": reference_year
        }

        logging.info(f"Generated band profile: {profile}")
        return profile

    except (AttributeError, IndexError, ValueError) as e:
        logging.error(f"Error parsing band profile response: {e}")
        raise ValueError("Failed to parse band profile from response.")
    
# Function to create a backstory for the band using ChatGPT
def create_band_backstory(band_profile):
    prompt = (
        f"Write a fan page backstory for a band called '{band_profile['Band Name']}' formed in {band_profile['Reference Year']} in {band_profile['Nationality']}. "
        f"The band has a {band_profile['Style Name']} style and blends {band_profile['Genre 1']} and {band_profile['Genre 2']} genres of music. "
        f"Include detailed descriptions of each band member and their instruments. "
        f"The completed backstory should be written in the style of {band_profile['Author Style']}. Limit the backstory to 250 words."
    )

    response = generate_chatgpt_response(prompt)

    # Log the backstory for debugging
    logging.info(f"Generated backstory: {response}")

    # Trim the response to ensure it is no longer than 250 words
    word_limit = 250
    words = response.split()
    
    if len(words) > word_limit:
        # Find the last complete sentence within the word limit
        trimmed_response = ' '.join(words[:word_limit])
        last_sentence_end = max(trimmed_response.rfind('.'), trimmed_response.rfind('!'), trimmed_response.rfind('?'))
        response = trimmed_response[:last_sentence_end + 1]
    
    return response

# Function to generate the discography using ChatGPT API
def generate_discography_info(band_profile, backstory):
    prompt = (
        f"Based on the following backstory and band profile, generate three unique and creative album titles for the band '{band_profile['Band Name']}'. "
        f"Each album should have a list of 10 to 15 tracks that fit the band's style, genres ({band_profile['Genre 1']} and {band_profile['Genre 2']}), and era ({band_profile['Reference Year']}). "
        f"The track names should be imaginative and reflect the band's evolution and changing themes over time. "
        f"Backstory: {backstory} "
        f"Ensure each album title is distinct, and the track names are varied and expressive, capturing different moods and stories."
    )

    response = generate_chatgpt_response(prompt)
    
    logging.info(f"Generated discography response: {response}")

    try:
        # Parse the response to extract album titles and track lists
        albums = []
        album_blocks = response.split("\n\n")  # Split response by double newlines to separate albums
        for album_block in album_blocks:
            lines = album_block.split("\n")
            title = lines[0].strip()
            tracks = []
            for line in lines[1:]:
                track = line.strip()
                if track:
                    tracks.append(track)
            albums.append((title, tracks))
        
        logging.info(f"Parsed albums: {albums}")
        return albums

    except Exception as e:
        logging.error(f"Error parsing discography response: {e}")
        raise

# Function to generate ChatGPT response for backstory or album descriptions
def generate_chatgpt_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        raise

# Function to extract band members from the backstory
def extract_band_members_from_backstory(backstory):
    try:
        # Regular expression pattern to match 'Firstname "Nickname" Lastname' format followed by instruments
        pattern = r'([A-Z][a-z]+\s"[^"]+"\s[A-Z][a-z]+)\s(?:with\s)?(?:on\s)?(\b(?:\w+\s?)+?(?:guitar|drums|vocals|bass|keys|piano|saxophone|trumpet|violin|flute|harmonica|synthesizer|accordion|banjo|mandolin|cello|percussion|congas|clarinet)\b)'
        
        # Find all matches of the pattern in the backstory
        matches = re.findall(pattern, backstory)

        logging.info(f"Extracted band members from backstory: {matches}")

        # Create band member dictionary
        band_members = []
        for match in matches:
            full_name = match[0].strip()
            instrument = match[1].strip()
            #bio = f"**{full_name}** is known for their expertise in {instrument} and adds a unique flavor to the band's music."
            bio = f"{full_name} on {instrument}"
            band_members.append({
                "name": full_name,
                "instruments": instrument,
                "bio": bio
            })

        return band_members

    except Exception as e:
        logging.error(f"Error extracting band members from backstory: {e}")

# Function to generate DALL-E images for band photo
def generate_dall_e_image(prompt, output_path):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful

        # Get the image URL from the response
        image_url = response.json()['data'][0]['url']

        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # Save the image to the specified output path
        with open(output_path, 'wb') as file:
            file.write(image_response.content)

        logging.info(f"Image saved to {output_path}")

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while generating image: {http_err}")
        raise
    except Exception as err:
        logging.error(f"An error occurred while generating image: {err}")
        raise

# Function to create HTML content with improved styling and band members section
def create_html_content(band_profile, backstory, albums, band_members, output_dir):
    selected_font = random.choice([
        "Arial, sans-serif", "Georgia, serif", "Tahoma, sans-serif", 
        "Verdana, sans-serif", "Trebuchet MS, sans-serif", "Courier New, monospace",
        "Lucida Sans, sans-serif", "Garamond, serif", "Helvetica, sans-serif"
    ])  # Randomly select a font
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{band_profile['Band Name']} - {band_profile['Style Name']} Sound</title>
        <style>
            body {{
                font-family: {selected_font};
                background-color: #F0E68C;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #2F4F4F;
                color: #FFF;
                padding: 20px;
                text-align: center;
            }}
            header h1 {{
                font-size: 3em;
                font-weight: bold;
                margin: 0;
                font-family: {selected_font};
            }}
            nav {{
                background-color: #8B4513;
                padding: 10px;
                text-align: center;
            }}
            nav a {{
                color: #FFF;
                margin: 0 15px;
                text-decoration: none;
                font-family: {selected_font};
            }}
            .container {{
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            .section-title {{
                font-family: {selected_font};
                font-size: 2em;
                border-bottom: 2px solid #333;
                padding-bottom: 5px;
                margin-bottom: 20px;
            }}
            .album-item {{
                margin-bottom: 20px;
            }}
            .album-item p {{
                margin: 0;
                font-size: 1em;
                color: #555;
            }}
            .track-list {{
                margin-top: 10px;
                padding-left: 20px;
                list-style-type: decimal;
            }}
            .band-member {{
                display: flex;
                align-items: center;
                margin-bottom: 20px;
            }}
            .band-member img {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                margin-right: 20px;
                border: 3px solid #8B4513;
            }}
            .band-member p {{
                margin: 0;
                font-size: 1.2em;
                font-weight: bold;
            }}
            .band-member-bio {{
                margin: 10px 0;
                font-size: 1em;
                color: #555;
            }}
            footer {{
                background-color: #2F4F4F;
                color: #FFF;
                text-align: center;
                padding: 10px 0;
                position: fixed;
                bottom: 0;
                width: 100%;
            }}
            .band-photo {{
                width: 600px;
                height: auto;
                display: block;
                margin: 0 auto 10px auto;
            }}
            .caption {{
                text-align: center;
                font-size: 1.1em;
                font-style: italic;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>

    <header>
        <h1>{band_profile['Band Name']} - {band_profile['Style Name']} Sound</h1>
    </header>

    <nav>
        <a href="#backstory">Backstory</a>
        <a href="#members">Band Members</a>
        <a href="#discography">Discography</a>
    </nav>

    <div class="container">
        <section id="backstory" class="backstory">
            <h2 class="section-title">Backstory</h2>
            <p>{backstory}</p>
        </section>

        <section id="members" class="members">
            <h2 class="section-title">Band Members</h2>
            <img src="band_photo.jpg" alt="{band_profile['Band Name']} Photo" class="band-photo">
            <div class="caption">Band Members: {', '.join(member['name'] for member in band_members)}</div>
            <div>
    """
    for i, member in enumerate(band_members):
        html_content += f"""
        <div class="band-member">
            <div>
                <p>{member['bio']}</p>
            </div>
        </div>
        """

    html_content += """
            </div>
        </section>

        <section id="discography" class="discography">
            <h2 class="section-title">Discography</h2>
    """
    for i, (title, tracks) in enumerate(albums):
        html_content += f"""
        <div class="album-item">
            <p><strong>{title}</strong></p>
            <ol class="track-list">
        """
        for track in tracks:
            html_content += f"<li>{track}</li>"
        html_content += """
            </ol>
        </div>
        """
    html_content += f"""
        </section>
    </div>

    <footer>
        <p>&copy; {current_year} {band_profile['Band Name']}. All rights reserved.</p>
    </footer>

    </body>
    </html>
    """
    return html_content

# Function to save HTML content to a file
def save_html_to_file(content, output_dir, filename="home.html"):
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w") as file:
            file.write(content)
        logging.info(f"HTML file '{filename}' created successfully in directory '{output_dir}'.")
    except OSError as e:
        logging.error(f"Error writing HTML file '{filename}': {e}")
        raise

# Function to create a unique subdirectory name based on band name in camelCase
def create_project_directory(band_name):
    directory_name = ''.join(word.capitalize() for word in band_name.split())
    directory = directory_name
    counter = 1
    while os.path.exists(directory):
        directory = f"{directory_name}{counter}"
        counter += 1

    try:
        os.makedirs(directory)
        logging.info(f"Directory '{directory}' created for the project output.")
    except OSError as e:
        logging.error(f"Error creating directory '{directory}': {e}")
        raise

    return directory

# Example usage
if __name__ == "__main__":
    try:
        # Generate a band profile using ChatGPT API
        band_profile = generate_band_profile()

        # Create project directory using camelCase band name
        output_dir = create_project_directory(band_profile['Band Name'])

        # Create band backstory using ChatGPT API
        backstory = create_band_backstory(band_profile)

        # Extract band member information from the generated backstory
        band_members = extract_band_members_from_backstory(backstory)

        # Generate discography information using ChatGPT API with enhanced creativity and uniqueness
        albums = generate_discography_info(band_profile, backstory)

        # Generate a single band photo using DALL-E
        band_photo_prompt = (
            f"A promotional photo of the band '{band_profile['Band Name']}' from {band_profile['Reference Year']}: "
            f"{', '.join(member['name'] for member in band_members)}. The image should be a traditional band promotional photo from a typical press kit of {band_profile['Reference Year']}, depicting them together, "
            f"reflecting their {band_profile['Style Name']} vibe & style of {band_profile['Reference Year']}, with elements of {band_profile['Genre 1']} and {band_profile['Genre 2']} attire and atmosphere."
        )
        band_photo_path = os.path.join(output_dir, "band_photo.jpg")
        generate_dall_e_image(band_photo_prompt, band_photo_path)

        # Create HTML content with improved styling and discography section
        html_content = create_html_content(band_profile, backstory, albums, band_members, output_dir)

        # Save HTML content to a file
        save_html_to_file(html_content, output_dir)

        logging.info("Script executed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during script execution: {e}")

    logging.info("Script execution ended.")
