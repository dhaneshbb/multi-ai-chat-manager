# Multi-AI Chat Manager Chrome Extension

This Chrome extension is a required component for the Multi-AI Chat Manager application. It automatically focuses the chat input fields when the application sends prompts via Ctrl+V.

## Installation

1. Open Google Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Select this folder containing `manifest.json` and `content.js`
6. Verify the extension appears in your extensions list

## Supported Platforms

- ChatGPT (chatgpt.com, chat.openai.com)
- Claude (claude.ai)
- Google Gemini (gemini.google.com)
- Perplexity (perplexity.ai)
- Grok (grok.com, x.com/i/grok)
- DeepSeek (chat.deepseek.com)
- Microsoft Copilot (copilot.microsoft.com)

## How It Works

1. The extension detects when you press Ctrl+V on any supported AI chat website
2. If you're not already in an input field, it automatically focuses the chat input
3. This ensures prompts from the Multi-AI Chat Manager paste correctly

## Features

- Platform-specific input field detection
- Smart cursor positioning
- Single Page Application (SPA) support
- Non-intrusive operation
- Debug logging for troubleshooting

## Troubleshooting

**Extension not working:**
- Ensure Developer mode is enabled
- Check that the extension is enabled in chrome://extensions/
- Refresh AI chat pages after installing
- Check browser console (F12) for error messages

**Prompts not pasting:**
- Verify the extension is active on the current tab
- Try refreshing the AI chat page
- Check if the AI platform updated their interface

## Privacy

This extension:
- Only activates on specified AI chat websites
- Does not collect or transmit any data
- Only focuses input fields when Ctrl+V is pressed
- Operates entirely locally in your browser

## Version

v1.0.0 - Professional release for Multi-AI Chat Manager