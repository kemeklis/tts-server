# TTS Server

A Text-to-Speech (TTS) project with a server-client architecture that supports both macOS and Linux.

## Table of Contents

- [TTS Server](#tts-server)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Dependencies with Poetry](#2-install-dependencies-with-poetry)
    - [3. Linux-Specific Steps](#3-linux-specific-steps)
  - [Usage](#usage)
    - [1. Running the TTS Server](#1-running-the-tts-server)
    - [2. Using the Clipboard Script](#2-using-the-clipboard-script)
      - [macOS](#macos)
      - [Linux](#linux)
      - [Binding to Keyboard Shortcut](#binding-to-keyboard-shortcut)
        - [macOS](#macos-1)
        - [Linux](#linux-1)
  - [API Endpoints](#api-endpoints)
  - [Project Structure](#project-structure)
  - [License](#license)
  - [Contact](#contact)

---

## Overview

This project provides a Flask-based Text-to-Speech (TTS) server that receives text input via a REST API or clipboard integration, synthesizes speech using a pre-trained TTS model, and plays the generated audio. The server can be controlled using API endpoints to start synthesis, stop playback, and check the playback status. It includes scripts for macOS and Linux to automate the process of sending clipboard content for synthesis, making it easy to speak copied text on demand.

---

## Features

- **Cross-Platform Support:** Works seamlessly on both macOS and Linux.
- **Clipboard Integration:** Reads text from the clipboard and synthesizes speech automatically.
- **Caching Mechanism:** Caches the TTS model after the first load to improve performance on subsequent requests.
- **Asynchronous Audio Playback:** Ensures that audio playback does not block other server operations.
- **RESTful API:** Offers endpoints for text synthesis, playback control, and status checking.
- **Health Check Endpoint:** Provides a health check endpoint to ensure the server is running properly.
- **Customizable Speed:** Allows adjustment of speech speed during synthesis.

---

## Prerequisites

- **Python:** Version 3.10.x
- **Poetry:** For dependency management and virtual environment handling. Install Poetry following the [official guide](https://python-poetry.org/docs/#installation).
- **Git:** For cloning the repository.
- **System Dependencies:**
  - **macOS:** No additional system dependencies required.
  - **Linux:**
    - `xclip` for clipboard access.
    - `portaudio` for audio playback.
    - Proper audio group permissions.

---

## Installation

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/yourusername/tts-server.git
cd tts-server
```

### 2. Install Dependencies with Poetry

Ensure that you have Poetry installed. If not, install it using the instructions provided in the [official documentation](https://python-poetry.org/docs/#installation).

Install the project dependencies by running:

```bash
poetry install
```

This command will:

- Create a virtual environment.
- Install all required Python packages specified in `pyproject.toml`.

### 3. Linux-Specific Steps

For Linux users, additional system dependencies are required:

1. **Install System Dependencies:**

   ```bash
   sudo pacman -S xclip portaudio
   ```

2. **Audio Permissions:**

   Add your user to the `audio` group to ensure proper audio permissions:

   ```bash
   sudo usermod -aG audio $USER
   ```

   **Note:** You may need to log out and log back in to apply the group changes.

3. **PulseAudio Users (Optional):**

   If you're using PulseAudio, install `pulseaudio-alsa`:

   ```bash
   sudo pacman -S pulseaudio-alsa
   ```

---

## Usage

### 1. Running the TTS Server

Activate the Poetry virtual environment:

```bash
poetry shell
```

Run the TTS server:

```bash
python src/tts_server/server.py
```

The server will start and listen on `http://0.0.0.0:5000`.

**Note:** The first time you run the server, it will download and cache the TTS model, which may take some time.

### 2. Using the Clipboard Script

The clipboard scripts allow you to synthesize speech from the text currently in your clipboard.

#### macOS

Ensure the script is executable:

```bash
chmod +x scripts/tts_clipboard_mac.sh
```

Run the script:

```bash
./scripts/tts_clipboard_mac.sh
```

#### Linux

Ensure the script is executable:

```bash
chmod +x scripts/tts_clipboard_linux.sh
```

Run the script:

```bash
./scripts/tts_clipboard_linux.sh
```

**Note:** The script will:

- Read the current clipboard content.
- Send the text to the TTS server for synthesis.
- Play the synthesized audio.

#### Binding to Keyboard Shortcut

To enhance usability, you can bind the clipboard script to a keyboard shortcut, allowing you to quickly synthesize copied text.

##### macOS

1. Open **System Preferences** and navigate to **Keyboard** > **Shortcuts**.
2. Click on **Services** and add a new service.
3. Use **Automator** to create a custom script that runs `scripts/tts_clipboard_mac.sh`.
4. Assign a keyboard shortcut to trigger the script.

##### Linux

1. Open **System Settings** and navigate to **Keyboard** > **Shortcuts**.
2. Add a new custom shortcut.
3. Set the command to `scripts/tts_clipboard_linux.sh`.
4. Assign a keyboard shortcut to trigger the script.

---

## API Endpoints

- **`POST /synthesize`**: Synthesizes speech from provided text.
  - **Payload:** JSON object containing:
    - `"text"` (string): The text to synthesize.
    - `"speed"` (float, optional): The speed of the speech (default is `4.0`).
  - **Example:**

    ```json
    {
      "text": "Hello, world!",
      "speed": 4.0
    }
    ```

- **`POST /stop`**: Stops the current audio playback.
  - **Usage:** Send a POST request with no payload to stop playback.

- **`GET /status`**: Checks if audio is currently playing.
  - **Response:** JSON object indicating the status.
    - `"status"`: `"playing"` or `"stopped"`

- **`GET /health`**: Checks if the server is running properly.
  - **Response:** JSON object indicating the health status.
    - `"status"`: `"healthy"`

---

## Project Structure

```
tts-server/
├── poetry.lock
├── pyproject.toml
├── README.md
├── scripts
│   ├── tts_clipboard_mac.sh
│   └── tts_clipboard_linux.sh
└── src
    └── tts_server
        ├── __init__.py
        └── server.py
```

---

## License

This project is licensed under the MIT License.

---

## Contact

Feel free to contribute to the project by opening issues or submitting pull requests.

