<div align="center">

# Mousiké

**Your Spotify stats, beautifully visualized.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Spotify API](https://img.shields.io/badge/Spotify_API-OAuth_2.0-1DB954?style=flat-square&logo=spotify&logoColor=white)](https://developer.spotify.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Features](#-features) · [Screenshots](#-screenshots) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [Project Structure](#-project-structure) · [Roadmap](#-roadmap)

---

</div>

## Overview

**Mousiké** is a personal Spotify stats dashboard built with Python and Flask. It connects to your Spotify account via OAuth 2.0 and lets you explore your listening habits — top artists, favorite tracks, genre breakdown, and recently played songs — across different time periods.

This project was built as a full-stack exercise integrating REST API consumption, server-side rendering, session management, and responsive UI design.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎵 **Top Tracks & Artists** | See your most listened-to content ranked over 4 weeks, 6 months, or all time |
| 🎸 **Genre Breakdown** | Discover your musical taste through a genre frequency analysis |
| 🕐 **Recent Activity** | Browse your last played tracks at a glance |
| 👤 **User Profile** | View your Spotify profile, followed artists, and listening overview |
| 🔒 **Secure Auth** | Full OAuth 2.0 PKCE flow — your credentials never touch the server |
| 📱 **Responsive UI** | Clean, mobile-first interface built with Tailwind CSS |

---

## 🛠 Tech Stack

```
Backend   →  Python 3.8+ · Flask · Spotipy
Frontend  →  HTML5 · Tailwind CSS · Vanilla JS
Auth      →  Spotify OAuth 2.0 (PKCE)
API       →  Spotify Web API
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- A Spotify account
- A registered app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

---

### 1. Clone the repository

```bash
git clone https://github.com/Heyissac/spotify-stats-web.git
cd spotify-stats-web
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

```env
# .env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
FLASK_SECRET_KEY=a_long_random_secret_key
```

> **Where to get these?** Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard), open your app → _Settings_, and copy the Client ID and Client Secret. Add `http://localhost:5000/callback` as a Redirect URI.

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser and log in with Spotify. 🎧

---

## 📁 Project Structure

```
spotify-stats-web/
│
├── static/
│   ├── css/
│   │   ├── main.css              # Global styles & variables
│   │   ├── profile.css           # Profile page styles
│   │   ├── stats.css             # Stats page styles
│   │   └── token.css             # Auth/token page styles
│   └── js/
│       ├── main.js               # Shared client-side logic
│       ├── profile.js            # Profile page interactions
│       └── stats.js              # Stats page interactions
│
├── templates/
│   ├── base.html                 # Base layout (nav, footer)
│   ├── index.html                # Landing page
│   ├── profile.html              # User profile & overview
│   ├── detailed_stats.html       # Stats by time range
│   └── error.html                # Error page
│
├── app.py                        # Flask entry point & routes
├── config.py                     # Environment config & constants
├── spotify_api.py                # Spotify API integration layer
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
└── .gitignore
```

---

## ⚙️ How It Works

```
User → /login → Spotify OAuth → /callback → token saved in session
                                                         ↓
                                          /profile  →  Spotify API
                                          /stats    →  Spotify API
```

1. The user logs in via **Spotify OAuth 2.0**
2. An access token is stored securely in the **Flask session**
3. Authenticated routes use `spotipy` to query the **Spotify Web API**
4. The token is automatically **refreshed** if expired before each request
5. Data is passed to **Jinja2 templates** for server-side rendering

---

## 🗺 Roadmap

- [ ] Add `.env.example` file to the repo
- [ ] Deploy to Render / Railway (with live demo link)
- [ ] Add loading skeletons for API calls
- [ ] Export stats as shareable image
- [ ] Add audio features analysis (energy, danceability, valence)
- [ ] Dark / light theme toggle

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome.

1. Fork the project
2. Create your branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'feat: add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the [MIT License](LICENSE).

---

<div align="center">

Built by [Issac](https://github.com/Heyissac) · Powered by the [Spotify Web API](https://developer.spotify.com/documentation/web-api)

</div>
