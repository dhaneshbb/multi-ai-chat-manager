# Changelog

All notable changes to the Multi-AI Chat Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-07-30

### Added
- **Chrome Extension Integration** - Auto-focus functionality for AI chat input fields
- **Custom Grid Layout** - 3×2 arrangement with configurable AI app priorities
- **Dark Theme GUI** - Professional interface with tkinter
- **Input History Management** - Navigate previous prompts with Up/Down arrows
- **Multi-Monitor Support** - Configure preferred display for window arrangement
- **Individual App Management** - Click buttons to bring specific AI apps to front
- **Window State Management** - Proper minimize/restore functionality
- **Taskbar Integration** - Hide AI apps from taskbar, show only manager
- **Build System** - PyInstaller-based executable creation
- **Configuration Wizard** - Interactive setup via setup_config.py
- **Diagnostic Tools** - System testing with test_fixes.py
- **Comprehensive Logging** - Debug information for troubleshooting

### Supported AI Platforms
- ChatGPT (chatgpt.com, chat.openai.com)
- Claude (claude.ai)
- Google Gemini (gemini.google.com)
- Perplexity (perplexity.ai)
- Grok (grok.com, x.com/i/grok)
- DeepSeek (chat.deepseek.com)

### Technical Features
- **Clipboard-based Message Sending** - Reliable prompt distribution
- **Window Detection** - Smart AI application identification
- **Error Handling** - Graceful failure recovery
- **Configuration Management** - YAML-based settings
- **Cross-Window Focus Management** - Proper window restoration
- **SPA Support** - Handles dynamic page changes in AI sites

### Build Tools
- Standalone executable generation
- Version info embedding
- Dependency checking
- Distribution packaging

## [1.x.x] - Previous Versions

### Legacy Features
- Basic window management
- Simple prompt sending
- Manual configuration

---

## Version History Notes

**v2.0.0** represents a complete rewrite with:
- Chrome extension integration for reliability
- Professional GUI interface
- Advanced window management
- Comprehensive error handling
- Build and distribution system

For older versions, see git commit history.