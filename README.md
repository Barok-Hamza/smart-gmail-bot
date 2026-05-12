# Smart Gmail Bot

An automated Gmail inbox assistant built with Python and the Gmail API.

This project connects directly to Gmail using OAuth authentication and automatically organizes incoming emails by applying custom Gmail labels based on sender and subject analysis.

---

## Features

- Gmail API integration
- Secure OAuth authentication
- Automatic Gmail label creation
- Automatic email categorization
- Real-time inbox monitoring
- Background automation loop
- Processed email tracking
- Automatic Gmail label application
- Continuous inbox checking every 30 seconds

---

## Technologies Used

- Python
- Gmail API
- Google OAuth 2.0
- JSON
- Schedule Library

---

## Current Email Categories

The bot currently detects and categorizes emails into:

- Social
- Shopping
- Housing
- Tech Programs
- School
- Jobs
- Internships
- Priority

---

## How It Works

1. Connects securely to Gmail using OAuth
2. Reads recent inbox emails
3. Analyzes sender and subject data
4. Matches emails to categories
5. Applies Gmail labels automatically
6. Tracks processed emails to avoid duplicates
7. Repeats monitoring every 30 seconds

---

## Security

Sensitive authentication files are excluded using `.gitignore`:

- credentials.json
- token.json

---

## Future Improvements

- AI-powered email classification
- GPT-generated draft replies
- Recruiter/interview prioritization
- Cloud deployment
- Real-time Gmail push notifications
- Advanced email analytics

---

## Author

Barok Hamza