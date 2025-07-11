# AI Band Generator Web App

A modern, attractive web frontend for the AI Band Generator that creates fictional bands with complete profiles, backstories, discographies, and AI-generated photos.

## Features

- **Modern Web Interface**: Beautiful, responsive design with animations and modern UI/UX
- **Real-time Progress Tracking**: Watch as your band is generated with live progress updates
- **Band Gallery**: Browse all previously generated bands with attractive card layouts
- **Mobile Responsive**: Works perfectly on all devices
- **Interactive Elements**: Hover effects, smooth animations, and modern interactions

## Quick Start

1. **Set up your environment**:
   ```bash
   # Set your OpenAI API key
   export OPENAI_API_KEY='your_openai_api_key_here'
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web app**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to `http://localhost:5000`

## Web App Structure

```
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── generate.html     # Band generation page
│   └── gallery.html      # Band gallery page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # Frontend JavaScript
│   └── img/              # Images and placeholders
└── createAct.py          # Original band generation logic
```

## API Endpoints

- `GET /` - Landing page
- `GET /generate` - Band generation interface
- `GET /gallery` - Band gallery
- `POST /api/generate` - Start band generation
- `GET /api/status/<id>` - Check generation status
- `GET /band/<name>` - View specific band page

## Features Overview

### Landing Page
- Hero section with compelling copy
- Feature highlights
- "How it works" section
- Recent bands showcase
- Call-to-action sections

### Generation Page
- Interactive generation interface
- Real-time progress tracking with step indicators
- Success/error handling
- Direct links to generated bands

### Gallery Page
- Grid layout of all generated bands
- Hover effects and smooth transitions
- Pagination support (ready for future)
- Filter options (framework in place)

## Design Features

- **Modern Color Scheme**: Purple and pink gradients with clean design
- **Typography**: Orbitron for headings, Roboto for body text
- **Animations**: Smooth transitions, hover effects, and loading states
- **Responsive**: Mobile-first design that works on all screen sizes
- **Accessibility**: Proper contrast ratios and semantic HTML

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Orbitron, Roboto)

## Customization

### Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6c5ce7;
    --secondary-color: #fd79a8;
    --accent-color: #00b894;
    /* ... */
}
```

### Layout
Templates use Bootstrap 5 grid system and can be easily customized.

### Animations
All animations are defined in the CSS and can be modified or disabled.

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up environment variables**:
   ```bash
   export FLASK_ENV=production
   export OPENAI_API_KEY='your_key'
   ```

3. **Configure a reverse proxy** (nginx, Apache, etc.)

4. **Set up SSL/TLS** for HTTPS

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.