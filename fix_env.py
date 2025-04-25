#!/usr/bin/env python3
"""
Fix .env file issues, particularly multiline API keys.
This script reads the .env file, fixes any issues, and saves it back.
"""

import os
import re
import shutil
from pathlib import Path

def fix_env_file():
    """Read the .env file, fix any issues, and save it back."""
    env_path = Path('.') / '.env'
    backup_path = Path('.') / '.env.backup'
    
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path.absolute()}")
        return False
    
    # Create a backup
    shutil.copy2(env_path, backup_path)
    print(f"Created backup of .env file at {backup_path.absolute()}")
    
    # Read the content
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Fix the OpenAI API key
    pattern = r'OPENAI_API_KEY=(.*?)(?=\n[a-zA-Z]|$)'
    matches = re.search(pattern, content, re.DOTALL)
    
    if not matches:
        print("Could not find OPENAI_API_KEY in .env file")
        return False
    
    api_key_value = matches.group(1)
    
    # Fix multiline and whitespace issues
    fixed_api_key = re.sub(r'\s+', '', api_key_value)
    
    # Replace in the content
    new_content = re.sub(
        pattern, 
        f'OPENAI_API_KEY={fixed_api_key}', 
        content, 
        flags=re.DOTALL
    )
    
    # Write back to the file
    with open(env_path, 'w') as f:
        f.write(new_content)
    
    print(f"Fixed OpenAI API key in .env file")
    
    # Print sample of fixed key (censored)
    if len(fixed_api_key) > 11:
        censored_key = f"{fixed_api_key[:7]}...{fixed_api_key[-4:]}"
        print(f"API key format now: {censored_key}")
    
    return True

if __name__ == "__main__":
    if fix_env_file():
        print("Successfully fixed .env file")
    else:
        print("Failed to fix .env file") 