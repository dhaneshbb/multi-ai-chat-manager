# Contributing to Multi-AI Chat Manager

Thanks for your interest in improving this project! Here's how you can help.

## Getting Started

### Prerequisites
- Windows 10/11 (primary development platform)
- Python 3.8+
- Google Chrome (for extension testing)
- Git

### Development Setup
```bash
# Clone the repository
git clone https://github.com/dhaneshbb/multi-ai-chat-manager.git
cd multi-ai-chat-manager

# Install dependencies
pip install -r requirements.txt

# Install Chrome extension for testing
# Chrome → chrome://extensions/ → Developer mode → Load unpacked → Chrome Extension folder

# Run diagnostics
python "Build Tools/test_fixes.py"

# Run from source
python main.py
```

## How to Contribute

### 1. Bug Reports
Use GitHub Issues with:
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (Windows version, Python version)
- **Log files** from `logs/multi_ai_chat.log`
- **Screenshots** if applicable

### 2. Feature Requests
- Check existing issues first
- Describe the use case clearly
- Explain why it would be useful
- Consider implementation complexity

### 3. Code Contributions

#### Before You Start
- Check existing issues and PRs
- Discuss major changes in an issue first
- Make sure you can run the diagnostic tests

#### Development Guidelines

**Code Style:**
- Follow PEP 8 conventions
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and modular

**Testing:**
- Run `python "Build Tools/test_fixes.py"` before submitting
- Test on different Windows versions if possible
- Verify Chrome extension still works
- Test with different AI applications

**Logging:**
- Add appropriate logging for debugging
- Use existing logger: `logging.getLogger(__name__)`
- Log errors, warnings, and important state changes

#### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch** from main
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
   - Run diagnostic script
   - Test with multiple AI apps
   - Check Chrome extension functionality
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: new feature description"
   git commit -m "Fix: specific bug description"
   git commit -m "Update: component improvement"
   ```
6. **Update documentation** if needed
7. **Submit pull request**

## Project Architecture

### Core Components
- **main.py** - Application entry point and coordination
- **window_manager.py** - AI window detection and arrangement
- **gui_interface.py** - User interface (tkinter)
- **prompt_sender.py** - Message automation (clipboard-based)
- **input_history.py** - Prompt history management

### Chrome Extension
- **manifest.json** - Extension configuration
- **content.js** - Input field auto-focus functionality

### Build Tools
- **build_exe.py** - PyInstaller executable creation
- **setup_config.py** - Interactive configuration
- **test_fixes.py** - System diagnostics

## Common Development Tasks

### Adding New AI Platform Support

1. **Update config.yml** with new platform details
2. **Add keywords** for window detection in window_manager.py
3. **Add selectors** to Chrome extension content.js
4. **Test thoroughly** with the new platform
5. **Update documentation**

### Improving Window Management

1. **Focus on window_manager.py**
2. **Test with different screen configurations**
3. **Handle edge cases** (minimized, maximized, hidden windows)
4. **Maintain backward compatibility**

### Enhancing Chrome Extension

1. **Update content.js** with new selectors
2. **Test on all supported AI platforms**
3. **Handle SPA navigation changes**
4. **Add fallback selectors for robustness**

## Known Issues & Areas for Improvement

### Current Limitations
- Windows-only (uses Windows APIs)
- Chrome extension dependency
- Some AI sites change input selectors frequently
- UAC can interfere with window operations

### Areas Needing Work
- **Cross-platform support** (Mac/Linux)
- **Firefox extension** version
- **API-based integration** when available
- **Advanced prompt templating**
- **Response comparison features**
- **Better error recovery**

## Release Process

1. **Update version** in config.yml and main.py
2. **Update CHANGELOG.md** with new features/fixes
3. **Test build process** with build_exe.py
4. **Create release** with built executable
5. **Tag version** in git

## Getting Help

- **Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Code Review** - All PRs get reviewed before merging

## Code of Conduct

- Be respectful and constructive
- Focus on the technical aspects
- Help others learn and contribute
- Keep discussions on-topic

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Thanks for helping make Multi-AI Chat Manager better!*
