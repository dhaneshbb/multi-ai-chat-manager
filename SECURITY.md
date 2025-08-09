# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | Yes                |


## Security Considerations

### Application Security

**Multi-AI Chat Manager** uses several Windows APIs and automation techniques that may trigger security software:

- **Window Management** - Uses Windows API to control other applications
- **Clipboard Access** - Copies and pastes text via system clipboard
- **Process Automation** - Launches applications via shortcuts
- **File System Access** - Reads configuration and writes log files

### Chrome Extension Security

The Chrome extension operates with minimal permissions:
- **activeTab** permission only
- No data collection or transmission
- Only activates on specific AI platform domains
- No background scripts or persistent storage

### Data Privacy

**No Data Transmission:**
- All operations are local to your machine
- No network requests or data uploads
- No telemetry or analytics
- No user data collection

**Local Data Storage:**
- Input history stored locally in `input_history.txt`
- Configuration stored in `config.yml`
- Log files stored in `logs/` directory
- All data remains on your system

### Potential Security Concerns

#### False Positives
Some antivirus software may flag this application because it:
- Automates other applications
- Uses Windows APIs for window control
- Accesses clipboard data
- Launches external processes

**These are normal operations** for window management software.

#### Legitimate Risks
- **Clipboard Exposure** - Prompts temporarily stored in system clipboard
- **Window Focus** - Application can bring windows to foreground
- **Process Launching** - Can execute shortcut files specified in config
- **Log Files** - May contain prompts and system information

### Best Practices

**For Users:**
- Only run from trusted sources
- Review configuration files before use
- Keep input history private if it contains sensitive prompts
- Run with standard user privileges when possible
- Regularly update to latest version

**For Developers:**
- Never log sensitive information
- Validate all configuration inputs
- Handle errors gracefully without exposing system details
- Follow principle of least privilege
- Sanitize file paths and user inputs

## Reporting Security Vulnerabilities

### What to Report
- Security vulnerabilities in the application code
- Potential privacy issues
- Unsafe handling of user data
- Privilege escalation possibilities
- Dependency vulnerabilities

### How to Report

**For non-critical issues:**
- Open a GitHub issue with "Security" label
- Include detailed description and reproduction steps

**For critical vulnerabilities:**
- Email the maintainer privately (see repository for contact)
- Include: Detailed description, impact assessment, reproduction steps
- Please allow 48 hours for initial response

### What NOT to Report
- Antivirus false positives (these are expected)
- Windows UAC prompts (this is normal behavior)
- Chrome extension permissions (these are minimal and necessary)
- Network security scans of AI platforms (out of scope)

## Threat Model

### In Scope
- Application code vulnerabilities
- Configuration file security
- Chrome extension security
- Local data protection
- Process and file system interactions

### Out of Scope
- AI platform security (third-party services)
- Network transmission security (no network features)
- Operating system vulnerabilities
- Browser security (beyond extension scope)
- Physical access scenarios

## Secure Configuration

### Recommended Settings
```yaml
# In config.yml - security considerations
window:
  timing:
    launch_delay: 0.1    # Don't set to 0 (may cause issues)
    
history:
  save_to_file: false    # Disable if prompts are sensitive
  max_entries: 50        # Limit history size
  
# Verify shortcut paths point to legitimate applications
ai_apps:
  - shortcut: "C:\\Legitimate\\Path\\Only"
```

### File Permissions
- Ensure config.yml is not world-readable
- Protect log files if they contain sensitive information
- Review input_history.txt contents periodically

## Dependencies Security

**Python Dependencies:**
- PyYAML - Configuration parsing
- psutil - Process management
- pywin32 - Windows API access
- pyinstaller - Executable building

**Monitoring:**
- Dependencies are monitored for security updates
- Use `pip audit` to check for known vulnerabilities
- Update dependencies regularly

## Terms of Service Compliance

### User Responsibility
Users are responsible for ensuring compliance with AI platform Terms of Service:
- This software uses standard Windows clipboard and window management
- Some AI platforms may have restrictions on automation
- Users should review platform terms before use
- The software author assumes no liability for Terms of Service violations

### Distribution
This software is distributed under the MIT License. Users may freely use, modify, and distribute the software in accordance with the license terms.

Note: This application is designed for productivity and educational purposes. Users should ensure compliance with all applicable Terms of Service when using AI platforms.
