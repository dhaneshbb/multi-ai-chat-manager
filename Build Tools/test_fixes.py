#!/usr/bin/env python3
"""
Diagnostic Script for Multi-AI Chat Manager
Tests the fixes and validates system functionality
"""

import os
import sys
import yaml
import logging
import time

def test_imports():
    """Test all required imports"""
    print(" Testing imports...")
    
    imports_to_test = [
        ('win32gui', 'Windows GUI operations'),
        ('win32clipboard', 'Clipboard access'),
        ('win32con', 'Windows constants'),
        ('win32com.client', 'COM automation'),
        ('win32api', 'Windows API'),
        ('win32process', 'Process management'),
        ('psutil', 'System utilities'),
        ('yaml', 'YAML configuration'),
    ]
    
    all_passed = True
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"   {module} - {description}")
        except ImportError as e:
            print(f"   {module} - {description}: {e}")
            all_passed = False
    
    return all_passed

def test_config_file():
    """Test configuration file"""
    print("\n Testing configuration...")
    
    if not os.path.exists("config.yml"):
        print("   config.yml not found")
        return False
    
    try:
        with open("config.yml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("   Configuration file loaded successfully")
        
        # Check AI apps configuration
        ai_apps = config.get('ai_apps', [])
        enabled_apps = [app for app in ai_apps if app.get('enabled', True)]
        
        print(f"   Found {len(enabled_apps)} enabled AI applications:")
        
        shortcut_issues = 0
        for app in enabled_apps:
            shortcut_path = app.get('shortcut', '')
            if os.path.exists(shortcut_path):
                print(f"     {app['name']}: {shortcut_path}")
            else:
                print(f"     {app['name']}: {shortcut_path} (NOT FOUND)")
                shortcut_issues += 1
        
        if shortcut_issues == 0:
            print("   All shortcuts are valid")
        else:
            print(f"    {shortcut_issues} shortcuts need fixing")
        
        return shortcut_issues == 0
        
    except Exception as e:
        print(f"   Configuration error: {e}")
        return False

def test_clipboard():
    """Test clipboard functionality"""
    print("\n Testing clipboard...")
    
    try:
        import win32clipboard
        
        test_text = "Multi-AI Chat Manager Test"
        
        # Set clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(test_text)
        win32clipboard.CloseClipboard()
        
        # Read clipboard
        win32clipboard.OpenClipboard()
        clipboard_content = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        
        if clipboard_content == test_text:
            print("   Clipboard operations working correctly")
            return True
        else:
            print("   Clipboard content mismatch")
            return False
            
    except Exception as e:
        print(f"   Clipboard test failed: {e}")
        return False

def test_window_detection():
    """Test window detection"""
    print("\n Testing window detection...")
    
    try:
        import win32gui
        
        def enum_windows_proc(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((hwnd, title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_proc, windows)
        
        print(f"   Detected {len(windows)} visible windows")
        
        # Look for potential AI app windows
        ai_keywords = ['chatgpt', 'claude', 'gemini', 'perplexity', 'grok', 'deepseek']
        ai_windows = []
        
        for hwnd, title in windows:
            title_lower = title.lower()
            for keyword in ai_keywords:
                if keyword in title_lower:
                    ai_windows.append((hwnd, title))
                    break
        
        if ai_windows:
            print(f"   Found {len(ai_windows)} potential AI application windows:")
            for hwnd, title in ai_windows:
                print(f"    - {title}")
        else:
            print("    No AI application windows detected (launch AI apps first)")
        
        return True
        
    except Exception as e:
        print(f"   Window detection failed: {e}")
        return False

def test_com_automation():
    """Test COM automation for key sending"""
    print("\n Testing COM automation...")
    
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        print("   WScript.Shell object created successfully")
        
        # Test a safe key operation (just test the object, don't actually send keys)
        print("   COM automation is ready for key sending")
        return True
        
    except Exception as e:
        print(f"   COM automation failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print(" Multi-AI Chat Manager - Diagnostic Tests")
    print("=" * 50)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Configuration File", test_config_file),
        ("Clipboard Operations", test_clipboard),
        ("Window Detection", test_window_detection),
        ("COM Automation", test_com_automation),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"   Test '{test_name}' crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f" Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(" All tests passed! Your system should work correctly.")
        print("\n Next steps:")
        print("   1. Replace your prompt_sender.py with the fixed version")
        print("   2. Replace your window_manager.py with the improved version")
        print("   3. Run: pip install -r requirements.txt")
        print("   4. Launch your AI applications first")
        print("   5. Run: python main.py")
    else:
        print("  Some tests failed. Please fix the issues before running the main application.")
        
        if passed_tests < total_tests - 1:
            print("\n Quick fixes:")
            print("   1. Run: pip install -r requirements.txt")
            print("   2. Verify your shortcut paths in config.yml")
            print("   3. Run this diagnostic script again")

if __name__ == "__main__":
    main()