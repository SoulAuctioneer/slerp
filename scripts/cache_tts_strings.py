#!/usr/bin/env python3
"""
TTS String Cache Utility

This script scans all Python files in the project for TTS strings and pre-caches them
using the ElevenLabs TTS service. This helps reduce latency during gameplay by 
pre-generating all audio files.

Usage:
    python scripts/cache_tts_strings.py [--force] [--dry-run]
    
Options:
    --force     Force re-cache even if files already exist
    --dry-run   Show what would be cached without actually caching
"""

import os
import re
import sys
import argparse
import asyncio
from pathlib import Path
from typing import List, Set, Dict, Tuple

# Add the project root to the path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.speech_synthesiser import SpeechSynthesizer
from src.settings import (
    ELEVENLABS_API_KEY, 
    ELEVENLABS_VOICE_ID, 
    ELEVENLABS_MODEL_ID, 
    TTS_CACHE_DIR
)

class TTSStringExtractor:
    """Extracts TTS strings from Python files using pattern matching"""
    
    def __init__(self):
        self.tts_strings: Set[str] = set()
        self.sources: Dict[str, List[Tuple[str, int]]] = {}  # string -> [(file, line), ...]
        self.excluded_dirs = {'venv', '.git', '__pycache__', '.pytest_cache', 'node_modules'}
        
    def scan_directory(self, directory: Path):
        """Scan a directory recursively for Python files"""
        for file_path in directory.rglob("*.py"):
            if file_path.name.startswith('.'):
                continue
                
            # Skip virtual environment and other excluded directories
            if any(excluded_dir in file_path.parts for excluded_dir in self.excluded_dirs):
                continue
                
            # Only scan files in specific project directories
            if not self._is_project_file(file_path):
                continue
                
            self.scan_file(file_path)
    
    def _is_project_file(self, file_path: Path) -> bool:
        """Check if file is part of the actual project (not dependencies)"""
        # Convert to relative path from project root
        try:
            rel_path = file_path.relative_to(project_root)
            # Only include files in main project directories
            if rel_path.parts[0] in {'src', 'routines', 'lib', 'tests', 'scripts'}:
                return True
            # Include root-level Python files
            if len(rel_path.parts) == 1:
                return True
        except ValueError:
            pass
        return False
    
    def scan_file(self, file_path: Path):
        """Scan a single Python file for TTS strings"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                
            self._extract_synthesize_speech_strings(content, lines, file_path)
            self._extract_speech_text_constants(content, lines, file_path)
            self._extract_button_response_strings(content, lines, file_path)
            self._extract_diagnosis_strings(content, lines, file_path)
            
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
    
    def _extract_synthesize_speech_strings(self, content: str, lines: List[str], file_path: Path):
        """Extract strings from SYNTHESIZE_SPEECH calls"""
        # Pattern for: SYNTHESIZE_SPEECH", text="..."
        pattern = r'SYNTHESIZE_SPEECH"[^"]*text\s*=\s*"([^"]+)"'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            text = match.group(1).strip()
            if text:
                line_num = content[:match.start()].count('\n') + 1
                self._add_string(text, file_path, line_num)
        
        # Pattern for: "SYNTHESIZE_SPEECH", text=speech_text where speech_text is a variable
        # We need to find the variable assignment
        pattern = r'SYNTHESIZE_SPEECH"[^"]*text\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            var_name = match.group(1)
            # Find the assignment of this variable
            var_pattern = rf'{var_name}\s*=\s*"([^"]+)"'
            var_matches = re.finditer(var_pattern, content)
            
            for var_match in var_matches:
                text = var_match.group(1).strip()
                if text:
                    line_num = content[:var_match.start()].count('\n') + 1
                    self._add_string(text, file_path, line_num)
    
    def _extract_speech_text_constants(self, content: str, lines: List[str], file_path: Path):
        """Extract SPEECH_TEXT constants and speech_text variables"""
        # Pattern for: SPEECH_TEXT = "..."
        pattern = r'SPEECH_TEXT\s*=\s*"([^"]+)"'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            text = match.group(1).strip()
            if text:
                line_num = content[:match.start()].count('\n') + 1
                self._add_string(text, file_path, line_num)
        
        # Pattern for: speech_text = "..."
        pattern = r'speech_text\s*=\s*"([^"]+)"'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            text = match.group(1).strip()
            if text:
                line_num = content[:match.start()].count('\n') + 1
                self._add_string(text, file_path, line_num)
    
    def _extract_button_response_strings(self, content: str, lines: List[str], file_path: Path):
        """Extract response strings from button lambda functions"""
        # Pattern for: lambda: self.answer_selected("key", "response text")
        pattern = r'answer_selected\([^,]+,\s*"([^"]+)"\)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            text = match.group(1).strip()
            if text:
                line_num = content[:match.start()].count('\n') + 1
                self._add_string(text, file_path, line_num)
    
    def _extract_diagnosis_strings(self, content: str, lines: List[str], file_path: Path):
        """Extract diagnosis text from diagnosis_options arrays"""
        # Look for diagnosis options with "text" field
        pattern = r'"text":\s*"([^"]+)"'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            text = match.group(1).strip()
            if text:
                line_num = content[:match.start()].count('\n') + 1
                self._add_string(text, file_path, line_num)
    
    def _add_string(self, text: str, file_path: Path, line_num: int):
        """Add a TTS string to the collection"""
        # Clean up the text
        text = text.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
        text = text.strip()
        
        if not text:
            return
        
        # Filter out strings that are too short or not meaningful
        if len(text) < 3:
            return
        
        # Filter out strings that are just ellipsis or placeholder text
        if text in {'...', 'response text', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}:
            return
        
        # Filter out strings that look like code or configuration
        if text.startswith(('\\u', 'Pretty printed', 'Incorrectly sorted')):
            return
            
        self.tts_strings.add(text)
        
        if text not in self.sources:
            self.sources[text] = []
        self.sources[text].append((str(file_path), line_num))
    
    def get_all_strings(self) -> List[str]:
        """Get all discovered TTS strings"""
        return sorted(list(self.tts_strings))


class TTSCacheManager:
    """Manages TTS caching operations"""
    
    def __init__(self, force: bool = False, dry_run: bool = False):
        self.force = force
        self.dry_run = dry_run
        self.synthesizer = None
        
        if not dry_run:
            if not ELEVENLABS_API_KEY:
                raise ValueError("ELEVENLABS_API_KEY not set in environment")
            
            self.synthesizer = SpeechSynthesizer(
                api_key=ELEVENLABS_API_KEY,
                voice_id=ELEVENLABS_VOICE_ID,
                model_id=ELEVENLABS_MODEL_ID,
                cache_dir=TTS_CACHE_DIR
            )
    
    async def cache_strings(self, strings: List[str], sources: Dict[str, List[Tuple[str, int]]]):
        """Cache all TTS strings"""
        print(f"Found {len(strings)} unique TTS strings")
        
        if self.dry_run:
            print("\nDRY RUN - Would cache the following strings:")
            for i, text in enumerate(strings, 1):
                print(f"\n{i}. {text[:80]}{'...' if len(text) > 80 else ''}")
                for file_path, line_num in sources.get(text, []):
                    print(f"   Source: {file_path}:{line_num}")
            return
        
        print(f"\nCaching {len(strings)} TTS strings...")
        
        cached_count = 0
        error_count = 0
        
        for i, text in enumerate(strings, 1):
            print(f"\n[{i}/{len(strings)}] Processing: {text[:60]}{'...' if len(text) > 60 else ''}")
            
            try:
                # Check if already cached (unless force is True)
                if not self.force:
                    cache_key = self.synthesizer._generate_cache_key(text)
                    cache_path = self.synthesizer._get_cache_path(cache_key)
                    if cache_path.exists():
                        print(f"  Already cached: {cache_path.name}")
                        cached_count += 1
                        continue
                
                # Cache the string
                result = await self.synthesizer.synthesize_speech(text)
                
                if result:
                    print(f"  Cached: {result.name}")
                    cached_count += 1
                else:
                    print(f"  ERROR: Failed to cache")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ERROR: {e}")
                error_count += 1
        
        print(f"\nCaching complete!")
        print(f"Successfully cached: {cached_count}")
        print(f"Errors: {error_count}")
        print(f"Total strings: {len(strings)}")


def main():
    parser = argparse.ArgumentParser(description='Cache TTS strings for faster gameplay')
    parser.add_argument('--force', action='store_true', 
                       help='Force re-cache even if files already exist')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be cached without actually caching')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    
    args = parser.parse_args()
    
    print("TTS String Cache Utility")
    print("=" * 40)
    
    # Initialize extractor
    extractor = TTSStringExtractor()
    
    # Scan the project
    print("Scanning Python files for TTS strings...")
    extractor.scan_directory(project_root)
    
    # Get all strings
    strings = extractor.get_all_strings()
    
    if not strings:
        print("No TTS strings found!")
        return
    
    if args.verbose:
        print(f"\nFound strings:")
        for i, text in enumerate(strings, 1):
            print(f"{i}. {text}")
            for file_path, line_num in extractor.sources.get(text, []):
                print(f"   {file_path}:{line_num}")
    
    # Cache the strings
    cache_manager = TTSCacheManager(force=args.force, dry_run=args.dry_run)
    
    try:
        asyncio.run(cache_manager.cache_strings(strings, extractor.sources))
    except KeyboardInterrupt:
        print("\nCaching interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during caching: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 