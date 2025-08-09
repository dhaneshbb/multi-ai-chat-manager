# Usage Guide - Multi-AI Chat Manager v1.0.0

 guide for using the Multi-AI Chat Manager effectively.

## Getting Started

### Initial Launch
1. **Start Application**: Run `Multi-AI Chat Manager.exe` or `python src/multi_ai_chat/main.py`
2. **Wait for Initialization**: The application will launch your configured AI applications
3. **Window Arrangement**: AI windows will be automatically arranged in a grid layout
4. **Ready State**: Status will show "Ready!" when all systems are operational

### Interface Overview

The Multi-AI Chat Manager interface consists of:

- **Header**: Application title, version, and connection status
- **AI Selection**: Checkboxes to select which AI applications to target
- **AI Status**: Visual indicators showing the state of each AI application
- **Prompt Input**: Main text area for entering your prompts
- **Control Panel**: Buttons for sending prompts and managing windows
- **Status Bar**: Keyboard shortcuts and version information

## Core Functionality

### Selecting AI Applications

**Individual Selection**:
- Use checkboxes in the "Select AI Applications" section
- Check/uncheck specific AI models you want to target
- Only selected applications will receive your prompts

**Bulk Selection**:
- "Select All": Choose all available AI applications
- "Select None": Deselect all AI applications
- Useful for quickly changing your target set

### Sending Prompts

**Basic Usage**:
1. Select desired AI applications using checkboxes
2. Type your prompt in the main text area
3. Press `Enter` or click "Send to Selected AI Apps"
4. Watch as your prompt appears in all selected AI chat windows

**Advanced Prompting**:
- Use `Shift+Enter` for multi-line prompts
- Prompts are automatically saved to history
- Clear input area after successful send

### Window Management

**Grid Operations**:
- **Minimize All**: Hide all AI windows (keeps them running)
- **Maximize Grid**: Restore and arrange windows in grid layout
- **Individual Focus**: Click AI status buttons to bring specific apps to front

**Application Management**:
- **Reopen All**: Close and restart all AI applications
- **Close All**: Shut down all AI applications
- Use when applications become unresponsive

##  Workflows

### Comparative Analysis
1. Select multiple AI applications (e.g., ChatGPT, Claude, Gemini)
2. Send identical prompts to all selected AIs
3. Compare responses across different models
4. Use for research, fact-checking, or getting diverse perspectives

### Specialized Tasks
1. **Creative Writing**: Use Claude and ChatGPT for different writing styles
2. **Technical Questions**: Target Perplexity for research-backed answers
3. **Code Review**: Send code to multiple AIs for different approaches
4. **Brainstorming**: Use all available AIs for maximum idea generation

### Efficiency Optimization
1. **Morning Setup**: Use "Reopen All" to fresh-start all AI sessions
2. **Focus Mode**: Select only relevant AIs for specific tasks
3. **Quick Switching**: Use individual AI buttons to jump between responses
4. **Batch Processing**: Queue multiple prompts using history navigation

## Configuration Management

### Runtime Configuration
- AI selection persists during session
- Window arrangements are maintained
- Application remembers your preferences

### Persistent Settings
Edit `config.yml` for permanent changes:
- Default AI selection states
- Window grid layout preferences
- Timing and performance settings
- Display and monitor preferences

## Keyboard Shortcuts

### Primary Controls
- `Enter`: Send prompt to selected AI applications
- `Shift+Enter`: Create new line in prompt (for multi-line text)

### Window Management
- Use mouse clicks for window control operations
- All functions accessible via buttons for reliability

## Troubleshooting Usage Issues

### Prompt Sending Problems

**No Prompts Received**:
1. Verify AI applications are selected (checkboxes checked)
2. Ensure Chrome extension is installed and active
3. Check if AI windows are responsive
4. Try "Maximize Grid" to refresh window states

**Partial Delivery**:
1. Some AI applications may be unresponsive
2. Check individual AI status indicators
3. Use "Reopen All" if multiple apps are failing
4. Verify Chrome extension works on all platforms

### Window Management Issues

**Windows Not Arranging**:
1. Run application as Administrator
2. Check display settings in config.yml
3. Try "Maximize Grid" multiple times
4. Some applications resist automatic positioning

**Missing Windows**:
1. Use "Reopen All" to refresh application list
2. Check if shortcuts in config.yml are valid
3. Verify AI applications are actually launching
4. Review logs for launch errors

### Performance Optimization

**Slow Response**:
1. Reduce number of simultaneously selected AIs
2. Increase timing delays in config.yml
3. Close unnecessary background applications
4. Use single AI for quick tasks

**Memory Usage**:
1. Restart AI applications periodically using "Reopen All"
2. Close unused AI applications
3. Monitor system resources during operation

## Best Practices

### Prompt Design
- **Clear Questions**: Use specific, well-formed questions
- **Context Setting**: Provide necessary background information
- **Consistent Format**: Use similar phrasing for comparative analysis
- **Length Management**: Balance detail with readability

### AI Selection Strategy
- **Task-Specific**: Choose AIs based on their strengths
- **Redundancy**: Use multiple AIs for important decisions
- **Efficiency**: Select fewer AIs for routine tasks
- **Exploration**: Vary selection to discover AI capabilities

### Workflow Organization
- **Session Planning**: Decide on AI selection before starting
- **Batch Processing**: Group similar prompts together
- **Result Management**: Copy/save important responses promptly
- **System Maintenance**: Regular application restarts for stability

## Advanced Features

### Multi-Monitor Setup
- Configure preferred display in config.yml
- Grid layout adapts to monitor resolution
- Supports primary and secondary displays

### History Management
- Automatic prompt history saving
- Persistent across application sessions
- Stored in `data/input_history.txt`
- Manual history file management possible

### Integration Possibilities
- Use with productivity tools
- Integrate into research workflows
- Combine with note-taking applications
- Export prompts and responses for documentation

## Getting Help

### Diagnostic Information
- Check `logs/multi_ai_chat.log` for detailed operation logs
- Use setup configuration tool for validation
- Monitor Windows Event Viewer for system-level issues

### Common Solutions
- Restart application for most issues
- Reinstall Chrome extension if prompts fail
- Update AI application shortcuts if detection fails
- Run as Administrator for permission issues

---

For technical support, review the installation guide and troubleshooting sections, or check the application logs for specific error messages.
