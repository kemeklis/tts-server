#!/bin/bash

# Configuration
TTS_SERVER_URL="http://localhost:5000"
TTS_SYNTHESIZE_ENDPOINT="${TTS_SERVER_URL}/synthesize"
TTS_STOP_ENDPOINT="${TTS_SERVER_URL}/stop"
TTS_STATUS_ENDPOINT="${TTS_SERVER_URL}/status"
CLIPBOARD_FILE="/tmp/tts_clipboard.txt"
PREV_CLIPBOARD_FILE="/tmp/tts_prev_clipboard.txt"

# Function to get the current clipboard content
get_clipboard_content() {
    pbpaste
}

# Function to send text to TTS server for synthesis
synthesize_text() {
    local text="$1"
    # Use jq to safely encode the text into valid JSON
    json_payload=$(jq -n --arg text "$text" '{text: $text}')
    curl -X POST "${TTS_SYNTHESIZE_ENDPOINT}" -H "Content-Type: application/json" -d "${json_payload}"
}

# Function to stop TTS playback
stop_playback() {
    curl -X POST "${TTS_STOP_ENDPOINT}"
}

# Function to check TTS server status
check_status() {
    curl -s "${TTS_STATUS_ENDPOINT}" | grep -o '"status":"playing"'
}

# Main logic

# Get the current clipboard content
clipboard_text=$(get_clipboard_content)
echo "Clipboard content: $clipboard_text"

# Save current clipboard content to file
echo "$clipboard_text" > "$CLIPBOARD_FILE"

# Check if previous clipboard content file exists
if [ -f "$PREV_CLIPBOARD_FILE" ]; then
    last_clipboard_text=$(cat "$PREV_CLIPBOARD_FILE")
else
    last_clipboard_text=""
fi

# Check if the clipboard content has changed
if [ "$clipboard_text" != "$last_clipboard_text" ]; then
    # If the clipboard content has changed and TTS is playing, stop it
    if check_status; then
        stop_playback
    fi
    # Start synthesis with new clipboard content
    synthesize_text "$clipboard_text"
else
    # If the clipboard content is the same, check TTS status
    if check_status; then
        # If TTS is playing, stop it
        stop_playback
    else
        # If TTS is not playing, start synthesis
        synthesize_text "$clipboard_text"
    fi
fi

# Save the current clipboard content as previous clipboard content
echo "$clipboard_text" > "$PREV_CLIPBOARD_FILE"
