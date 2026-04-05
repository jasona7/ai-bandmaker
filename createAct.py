import os
import json
import random
import html
import requests
import logging
from datetime import datetime

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


def generate_chatgpt_response(prompt, max_tokens=500, temperature=0.9):
    """Generate a ChatGPT response with configurable parameters."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        raise


def generate_band_profile(constraints=None):
    """Generate a completely unique band profile using AI, with optional user constraints."""
    constraints = constraints or {}

    # Build constraint instructions for fields the user locked in
    locked = []
    if constraints.get('genre1'):
        locked.append(f"Genre 1 MUST be: {constraints['genre1']}")
    if constraints.get('genre2'):
        locked.append(f"Genre 2 MUST be: {constraints['genre2']}")
    if constraints.get('nationality'):
        locked.append(f"Nationality MUST be: {constraints['nationality']}")
    if constraints.get('style_name'):
        locked.append(f"Style Name MUST be: {constraints['style_name']}")

    era_instruction = ""
    if constraints.get('era'):
        era_instruction = f"Reference Year MUST be between {constraints['era'].replace('-', ' and ')}."
    else:
        era_instruction = "Reference Year: pick any year between 1955 and 2020."

    constraint_block = ""
    if locked:
        constraint_block = "LOCKED FIELDS (use these exactly):\n" + "\n".join(f"- {l}" for l in locked) + "\n\n"

    prompt = (
        "You are a record store clerk who has spent 40 years digging through crates of obscure vinyl. "
        "You know about bands that never made it past their local scene, one-album wonders, "
        "cult acts that only got written about in fanzines. "
        "Invent a fictional band that feels like a real discovery — not an AI creation.\n\n"
        f"{constraint_block}"
        "RULES:\n"
        "- The band name should sound like something humans would actually name a band. "
        "Avoid AI-sounding names like 'The [Adjective] [Noun]' or 'Ethereal [Something]'. "
        "Think more like: Slint, Cocteau Twins, Os Mutantes, Fela Kuti, Broadcast, Stereolab, "
        "Neu!, Can, The Raincoats, Lingua Ignota — real bands with distinctive names.\n"
        "- The writing voice should be a real music critic (Lester Bangs, Simon Reynolds, Jessica Hopper, "
        "Kodwo Eshun, Greil Marcus, etc.) — NOT a generic 'passionate music journalist'.\n"
        "- Be specific about the region. Not just 'USA' — say where exactly.\n"
        "- Genres should be specific subgenres, not broad categories like 'rock' or 'electronic'.\n"
        f"- {era_instruction}\n\n"
        "Format your response EXACTLY like this (one field per line, no extra text):\n"
        "Band Name: [name]\n"
        "Author Style: [critic/voice]\n"
        "Nationality: [nationality]\n"
        "Genre 1: [genre]\n"
        "Genre 2: [genre]\n"
        "Style Name: [descriptor]\n"
        "Reference Year: [year]"
    )

    response = generate_chatgpt_response(prompt, max_tokens=200, temperature=1.3)
    logging.info(f"Raw band profile response: {response}")

    try:
        import re
        band_name = re.search(r"Band Name:\s*(.*)", response).group(1).strip()
        author_style = re.search(r"Author Style:\s*(.*)", response).group(1).strip()
        nationality = re.search(r"Nationality:\s*(.*)", response).group(1).strip()
        genre1 = re.search(r"Genre 1:\s*(.*)", response).group(1).strip()
        genre2 = re.search(r"Genre 2:\s*(.*)", response).group(1).strip()
        style_name = re.search(r"Style Name:\s*(.*)", response).group(1).strip()
        reference_year_str = re.search(r"Reference Year:\s*([^\n]*)", response).group(1).strip()
        reference_year = int(re.sub(r"[^\d]", "", reference_year_str))

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


def create_band_backstory(band_profile):
    """Create a detailed backstory with named band members."""
    prompt = (
        f"Write a fan page backstory for a fictional band called '{band_profile['Band Name']}' "
        f"formed around {band_profile['Reference Year']} in {band_profile['Nationality']}. "
        f"They have a {band_profile['Style Name']} style blending {band_profile['Genre 1']} and {band_profile['Genre 2']}.\n\n"
        f"IMPORTANT: Include exactly 3-5 band members. For EACH member, clearly state:\n"
        f"- Their full name (first and last, with an optional nickname in quotes)\n"
        f"- Their instrument or role (e.g., lead vocals, bass guitar, drums, synthesizer)\n"
        f"- A brief note about their personality or contribution\n\n"
        f"TONE: Write like an enthusiastic fan who saw them live, NOT like a music critic writing for an academic journal. "
        f"Use plain, conversational language. Tell a story — how they met, a funny anecdote, what it was like to see them play. "
        f"Avoid abstract descriptions, flowery metaphors, and phrases like 'sonic tapestry', 'ethereal soundscapes', "
        f"'transcendent', 'luminous', or 'ineffable'. Just tell us about the band like you're talking to a friend at a bar.\n\n"
        f"You can draw loosely on the voice of {band_profile['Author Style']} but keep it accessible. "
        f"Keep it to 250 words."
    )

    response = generate_chatgpt_response(prompt, max_tokens=600, temperature=0.9)
    logging.info(f"Generated backstory: {response}")

    # Trim to ~250 words at a sentence boundary
    words = response.split()
    if len(words) > 280:
        trimmed = ' '.join(words[:280])
        last_end = max(trimmed.rfind('.'), trimmed.rfind('!'), trimmed.rfind('?'))
        if last_end > 0:
            response = trimmed[:last_end + 1]

    return response


def extract_band_members(band_profile, backstory):
    """Use AI to extract structured band member info from the backstory."""
    prompt = (
        f"Read this backstory for the band '{band_profile['Band Name']}' and extract the band members.\n\n"
        f"Backstory:\n{backstory}\n\n"
        f"Return a JSON array of band members. Each member should have:\n"
        f"- \"name\": their full name (include nickname if mentioned)\n"
        f"- \"instrument\": their instrument or role\n"
        f"- \"bio\": a one-sentence description of them\n\n"
        f"Return ONLY valid JSON, no other text. Example format:\n"
        f'[{{"name": "Jane Doe", "instrument": "lead vocals", "bio": "The fiery frontwoman..."}}]'
    )

    response = generate_chatgpt_response(prompt, max_tokens=600, temperature=0.3)
    logging.info(f"Raw member extraction response: {response}")

    try:
        # Strip markdown code fences if present
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

        members = json.loads(cleaned)
        logging.info(f"Extracted band members: {members}")
        return members
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error parsing band members JSON: {e}")
        # Fallback: return a minimal member list
        return [{"name": band_profile["Band Name"], "instrument": "various", "bio": "The band."}]


def generate_discography_info(band_profile, backstory):
    """Generate a full discography with 3 albums and 10-15 tracks each."""
    prompt = (
        f"Generate a complete discography for the fictional band '{band_profile['Band Name']}' "
        f"({band_profile['Genre 1']}/{band_profile['Genre 2']}, {band_profile['Style Name']} style, "
        f"active around {band_profile['Reference Year']}).\n\n"
        f"Backstory context: {backstory[:300]}...\n\n"
        f"Create exactly 3 albums. For each album provide:\n"
        f"- An album title (creative, era-appropriate)\n"
        f"- 10-15 track names that reflect the band's evolution\n\n"
        f"Format EXACTLY like this (separate albums with a blank line):\n\n"
        f"Album: [Title] ([Year])\n"
        f"1. Track Name\n"
        f"2. Track Name\n"
        f"...\n\n"
        f"Album: [Title] ([Year])\n"
        f"1. Track Name\n"
        f"..."
    )

    response = generate_chatgpt_response(prompt, max_tokens=1500, temperature=0.85)
    logging.info(f"Generated discography response: {response}")

    try:
        albums = []
        album_blocks = response.split("\n\n")
        current_title = None
        current_tracks = []

        for block in album_blocks:
            lines = block.strip().split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.lower().startswith("album:") or (not line[0].isdigit() and not current_title):
                    # Save previous album if exists
                    if current_title and current_tracks:
                        albums.append((current_title, current_tracks))
                    current_title = line.replace("Album:", "").strip() if line.lower().startswith("album:") else line
                    current_tracks = []
                elif line and (line[0].isdigit() or line.startswith("-")):
                    # Strip leading number/dash/dot
                    import re
                    track = re.sub(r'^[\d]+[\.\)\-\s]+', '', line).strip()
                    track = re.sub(r'^[\-\s]+', '', track).strip()
                    if track:
                        current_tracks.append(track)

        # Don't forget the last album
        if current_title and current_tracks:
            albums.append((current_title, current_tracks))

        logging.info(f"Parsed {len(albums)} albums")
        return albums

    except Exception as e:
        logging.error(f"Error parsing discography response: {e}")
        raise


def get_era_fashion_description(reference_year):
    """Map a band's reference year to era-appropriate fashion and setting cues."""
    year = int(reference_year)
    if year < 1970:
        return "1950s-1960s fashion: slim suits, thin ties, pompadour hairdos or bouffants, vintage studio backdrop"
    elif year < 1980:
        return "1970s fashion: bell-bottoms, long hair, mustaches, open collars, wood-paneled or earthy studio backdrop"
    elif year < 1990:
        return "1980s fashion: big hair, leather jackets, bold makeup, denim, studio backdrop with dramatic lighting"
    elif year < 2000:
        return "1990s fashion: flannel, grunge, band t-shirts, Doc Martens, candid warehouse or alley setting"
    else:
        return "2000s-2010s fashion: contemporary streetwear, clean styling, urban or industrial backdrop"


def generate_dall_e_image(prompt, output_path):
    """Generate a DALL-E image and save it to disk."""
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
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        with open(output_path, 'wb') as file:
            file.write(image_response.content)

        logging.info(f"Image saved to {output_path}")

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while generating image: {http_err}")
        raise
    except Exception as err:
        logging.error(f"An error occurred while generating image: {err}")
        raise


def build_band_photo_prompt(band_profile, band_members):
    """Build a DALL-E prompt for a black and white band press photo."""
    fashion = get_era_fashion_description(band_profile['Reference Year'])
    member_count = len(band_members)

    prompt = (
        f"A professional black and white press kit photograph of {member_count} musicians "
        f"posing together as a band. Shot on medium-format film, high contrast, dramatic "
        f"studio lighting with deep shadows. {fashion}. "
        f"The band plays {band_profile['Genre 1']}/{band_profile['Genre 2']} and has a "
        f"{band_profile['Style Name']} aesthetic. "
        f"This should look like an authentic black and white promotional photo from a "
        f"music magazine circa {band_profile['Reference Year']}. "
        f"Photorealistic, film grain, no text or words in the image."
    )

    logging.info(f"DALL-E prompt: {prompt}")
    return prompt


def create_html_content(band_profile, backstory, albums, band_members, output_dir):
    """Generate a retro 90s-style fan page HTML for the band."""
    # Escape all AI-generated strings to prevent XSS (C-001)
    band_name = html.escape(band_profile['Band Name'])
    style_name = html.escape(band_profile['Style Name'])
    ref_year = int(band_profile['Reference Year'])
    genre1 = html.escape(band_profile['Genre 1'])
    genre2 = html.escape(band_profile['Genre 2'])
    nationality = html.escape(band_profile['Nationality'])
    backstory_escaped = html.escape(backstory)

    # Pick random retro accent colors
    accent_colors = [
        ("#00ffff", "#ff00ff", "#ffff00"),  # cyan, magenta, yellow
        ("#00ff00", "#ff6600", "#ff00ff"),  # lime, orange, magenta
        ("#ffff00", "#00ffff", "#ff4444"),  # yellow, cyan, red
        ("#ff69b4", "#00ff00", "#ffff00"),  # hotpink, lime, yellow
    ]
    c1, c2, c3 = random.choice(accent_colors)

    # Build members HTML (escape all AI-generated fields)
    members_html = ""
    for member in band_members:
        m_name = html.escape(member.get('name', 'Unknown'))
        m_instrument = html.escape(member.get('instrument', ''))
        m_bio = html.escape(member.get('bio', ''))
        members_html += f"""
        <tr>
            <td style="color:{c2}; padding:4px 12px; font-weight:bold;">{m_name}</td>
            <td style="color:{c3}; padding:4px 12px;">{m_instrument}</td>
        </tr>
        <tr>
            <td colspan="2" style="color:#cccccc; padding:2px 12px 8px 12px; font-size:0.9em;">{m_bio}</td>
        </tr>"""

    # Build discography HTML (escape all AI-generated fields)
    disco_html = ""
    for title, tracks in albums:
        title_escaped = html.escape(title)
        tracks_html = ""
        for i, track in enumerate(tracks, 1):
            tracks_html += f'<li style="color:#cccccc;">{html.escape(track)}</li>\n'
        disco_html += f"""
        <table width="90%" cellpadding="4" cellspacing="0" border="1" bordercolor="{c2}"
               style="margin:10px auto; background-color:#111111;">
            <tr><td colspan="2" style="background-color:#222222; color:{c1}; font-weight:bold; padding:8px; font-size:1.1em;">
                {title_escaped}
            </td></tr>
            <tr><td style="padding:8px;">
                <ol style="color:{c3}; margin:0; padding-left:20px;">
                    {tracks_html}
                </ol>
            </td></tr>
        </table>"""

    # Visitor counter (fake, random)
    visitor_count = random.randint(1247, 99999)

    # Escaped member names for photo caption
    member_names_escaped = ', '.join(html.escape(m.get('name', '')) for m in band_members)

    # Safe email-friendly band name (alphanumeric only)
    email_band = ''.join(c for c in band_profile['Band Name'] if c.isalnum()).lower()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>~*~ {band_name} ~*~ Official Fan Page ~*~</title>
    <style>
        body {{
            background-color: #000000;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='3' height='3'%3E%3Crect width='1' height='1' fill='%23111'/%3E%3C/svg%3E");
            color: #cccccc;
            font-family: 'Comic Sans MS', 'Trebuchet MS', cursive, sans-serif;
            margin: 0;
            padding: 0;
        }}
        a {{ color: {c1}; }}
        a:visited {{ color: {c2}; }}
        a:hover {{ color: {c3}; text-decoration: none; }}
        .skip-link {{
            position: absolute;
            left: -9999px;
            top: auto;
            width: 1px;
            height: 1px;
            overflow: hidden;
        }}
        .skip-link:focus {{
            position: fixed;
            top: 0;
            left: 0;
            width: auto;
            height: auto;
            padding: 8px 16px;
            background: #ffff00;
            color: #000;
            font-weight: bold;
            z-index: 100;
        }}
        .page-wrapper {{
            max-width: 800px;
            margin: 0 auto;
            padding: 10px;
        }}
        .header-table {{
            width: 100%;
            background: linear-gradient(to right, #000033, #000066, #000033);
            border: 3px ridge {c2};
            margin-bottom: 10px;
        }}
        .header-table td {{
            text-align: center;
            padding: 15px;
        }}
        .band-title {{
            font-size: 1.8em;
            font-weight: bold;
            color: {c1};
            text-shadow: 2px 2px 4px {c2};
            font-family: 'Impact', 'Arial Black', sans-serif;
        }}
        .divider {{
            width: 80%;
            margin: 15px auto;
        }}
        .section-header {{
            color: {c1};
            font-size: 1.3em;
            text-align: center;
            margin: 20px 0 10px 0;
            text-shadow: 1px 1px 2px {c2};
        }}
        .photo-frame {{
            text-align: center;
            margin: 15px auto;
            position: relative;
            display: inline-block;
        }}
        .photo-wrapper {{
            text-align: center;
        }}
        .photo-frame img {{
            max-width: 500px;
            width: 100%;
            border: 4px ridge {c2};
            display: block;
            filter: grayscale(100%);
        }}
        .photo-credit {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            color: #aaaaaa;
            font-size: 0.65em;
            font-family: 'Helvetica', 'Arial', sans-serif;
            text-shadow: 1px 1px 2px #000000;
            letter-spacing: 0.5px;
        }}
        .photo-caption {{
            color: {c3};
            font-style: italic;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .backstory-box {{
            background-color: #0a0a1a;
            border: 2px inset {c1};
            padding: 15px;
            margin: 10px auto;
            width: 90%;
            color: #dddddd;
            line-height: 1.6;
            font-size: 0.95em;
        }}
        .members-table {{
            margin: 10px auto;
            border: 2px ridge {c1};
            background-color: #0a0a0a;
            border-collapse: collapse;
        }}
        .members-table td {{
            border-bottom: 1px dashed #333333;
        }}
        .footer-area {{
            text-align: center;
            margin-top: 30px;
            padding: 15px;
            border-top: 2px ridge {c2};
            font-size: 0.8em;
            color: #888888;
        }}
        .footer-area a {{
            color: {c2};
            font-size: 0.85em;
        }}
        .blink {{
            animation: blinker 1.2s linear infinite;
        }}
        @keyframes blinker {{
            50% {{ opacity: 0; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .blink {{
                animation: none;
            }}
        }}
        .badge-row {{
            text-align: center;
            margin: 15px 0;
            font-size: 0.75em;
            color: #aaaaaa;
        }}
        .badge-row span {{
            margin: 0 8px;
            padding: 3px 8px;
            border: 1px solid #444444;
            background-color: #111111;
        }}
        .nav-bar {{
            text-align: center;
            padding: 8px;
            background-color: #111111;
            border: 1px solid #333333;
            margin-bottom: 10px;
            font-size: 0.95em;
        }}
        .nav-bar a {{
            margin: 0 5px;
        }}
        @media (max-width: 600px) {{
            .band-title {{
                font-size: 1.2em !important;
            }}
            .header-table {{
                width: 100% !important;
            }}
            .members-table {{
                width: 100% !important;
            }}
            .nav-bar {{
                display: flex;
                flex-direction: column;
                gap: 4px;
            }}
            .nav-bar a {{
                display: block;
                margin: 2px 0;
            }}
        }}
        .stars {{
            color: {c3};
            letter-spacing: 3px;
        }}
    </style>
</head>
<body>

<a href="#main" class="skip-link">Skip to main content</a>

<div class="page-wrapper">

    <!-- Header -->
    <header>
    <table class="header-table" cellpadding="0" cellspacing="0">
        <tr><td>
            <span class="stars" aria-hidden="true">* * * * * * * * * * * * *</span><br>
            <h1 class="band-title">{band_name}</h1>
            <span style="color:{c3}; font-size:0.85em;">
                {style_name} | {genre1} / {genre2} | Est. {ref_year} | {nationality}
            </span><br>
            <span class="stars" aria-hidden="true">* * * * * * * * * * * * *</span>
        </td></tr>
    </table>
    </header>

    <!-- Navigation -->
    <nav class="nav-bar" aria-label="Page sections">
        <a href="#backstory">Backstory</a> |
        <a href="#photo">Band Photo</a> |
        <a href="#members">Members</a> |
        <a href="#discography">Discography</a> |
        <a href="#guestbook">Guestbook</a>
    </nav>

    <main id="main">

    <!-- Backstory -->
    <h2 id="backstory" class="section-header">~ The Story ~</h2>
    <hr class="divider" color="{c2}" size="2" noshade>
    <div class="backstory-box">
        {backstory_escaped}
    </div>

    <!-- Band Photo -->
    <h2 id="photo" class="section-header">~ Band Photo ~</h2>
    <hr class="divider" color="{c2}" size="2" noshade>
    <div class="photo-wrapper">
        <div class="photo-frame">
            <img src="band_photo.jpg" alt="Promotional photo of {band_name}">
            <div class="photo-credit">Mgmt: {band_name.split()[0] if ' ' in band_name else band_name} Artists Group / {nationality}</div>
        </div>
        <div class="photo-caption">
            {member_names_escaped}
        </div>
    </div>

    <!-- Band Members -->
    <h2 id="members" class="section-header">~ The Members ~</h2>
    <hr class="divider" color="{c2}" size="2" noshade>
    <table class="members-table" cellpadding="0" cellspacing="0" width="90%">
        {members_html}
    </table>

    <!-- Discography -->
    <h2 id="discography" class="section-header">~ Discography ~</h2>
    <hr class="divider" color="{c2}" size="2" noshade>
    {disco_html}

    <!-- Guestbook / Links -->
    <h2 id="guestbook" class="section-header">~ Guestbook &amp; Links ~</h2>
    <hr class="divider" color="{c2}" size="2" noshade>
    <div style="text-align:center; padding:10px;">
        <p><a href="#">Sign the Guestbook!</a> | <a href="#">View Guestbook</a></p>
        <p><a href="mailto:webmaster@{email_band}.geocities.com">Email the Webmaster</a></p>
        <p style="color:#888888; font-size:0.8em;">
            <a href="#">Link to us!</a> |
            <a href="#">Webrings</a> |
            <a href="#">MIDI Archive</a>
        </p>
    </div>

    </main>

    <!-- Badges / Footer -->
    <footer>
    <div class="badge-row" aria-hidden="true">
        <span>Best viewed in Netscape Navigator 4.0</span>
        <span>800x600 resolution</span>
        <span>Made with Notepad</span>
    </div>

    <div class="footer-area">
        <p aria-hidden="true">You are visitor number <strong style="color:{c1};">#{visitor_count:,}</strong> since {ref_year}!</p>
        <p class="blink">*** This page is always under construction! ***</p>
        <p>&copy; {current_year} {band_name} Fan Page. All rights reserved.<br>
        This is a fan-made page. We are not affiliated with {band_name} or their management.</p>
        <p><a href="#">Back to Top</a> | <a href="/">Back to AI Band Generator</a></p>
    </div>
    </footer>

</div>

</body>
</html>"""
    return html_content


def save_html_to_file(content, output_dir, filename="home.html"):
    """Save HTML content to a file."""
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w") as file:
            file.write(content)
        logging.info(f"HTML file '{filename}' created successfully in directory '{output_dir}'.")
    except OSError as e:
        logging.error(f"Error writing HTML file '{filename}': {e}")
        raise


def create_project_directory(band_name):
    """Create a unique subdirectory based on band name in CamelCase."""
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


# CLI entry point
if __name__ == "__main__":
    try:
        # Generate a band profile
        band_profile = generate_band_profile()

        # Create project directory
        output_dir = create_project_directory(band_profile['Band Name'])

        # Create band backstory
        backstory = create_band_backstory(band_profile)

        # Extract band members via AI
        band_members = extract_band_members(band_profile, backstory)

        # Generate discography
        albums = generate_discography_info(band_profile, backstory)

        # Generate band photo with era-appropriate styling
        photo_prompt = build_band_photo_prompt(band_profile, band_members)
        band_photo_path = os.path.join(output_dir, "band_photo.jpg")
        generate_dall_e_image(photo_prompt, band_photo_path)

        # Create and save the HTML fan page
        html_content = create_html_content(band_profile, backstory, albums, band_members, output_dir)
        save_html_to_file(html_content, output_dir)

        logging.info("Script executed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during script execution: {e}")

    logging.info("Script execution ended.")
