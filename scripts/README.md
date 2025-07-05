# TTS Cache Utility Scripts

This directory contains utility scripts for managing TTS (Text-to-Speech) assets in the Slerp project.

## cache_tts_strings.py

A utility script that automatically scans all Python files in the project to find TTS strings and pre-caches them using the ElevenLabs TTS service. This helps reduce latency during gameplay by pre-generating all audio files.

### Features

- **Intelligent Pattern Matching**: Uses multiple regex patterns to find TTS strings in various formats:
  - Direct `SYNTHESIZE_SPEECH` event calls
  - `SPEECH_TEXT` constants
  - `speech_text` variables
  - Button response texts in lambda functions
  - Diagnosis text from diagnosis options
  
- **Smart Filtering**: Automatically filters out:
  - Virtual environment files
  - Third-party library files
  - Short or meaningless strings
  - Code artifacts and configuration text
  
- **Comprehensive Scanning**: Scans all relevant project directories:
  - `src/` - Main application code
  - `routines/` - Game routine scripts
  - `lib/` - Custom libraries
  - `tests/` - Test files
  - `scripts/` - Utility scripts

### Prerequisites

1. **ElevenLabs API Key**: Make sure you have your ElevenLabs API key set in the environment:
   ```bash
   export ELEVENLABS_API_KEY=your_api_key_here
   ```

2. **Python Dependencies**: Ensure all required packages are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Basic Usage

```bash
# Preview what would be cached (recommended first run)
python scripts/cache_tts_strings.py --dry-run

# Cache all discovered TTS strings
python scripts/cache_tts_strings.py

# Force re-cache even if files already exist
python scripts/cache_tts_strings.py --force

# Show detailed output with all found strings
python scripts/cache_tts_strings.py --dry-run --verbose
```

#### Command Line Options

- `--dry-run`: Show what would be cached without actually caching
- `--force`: Force re-cache even if files already exist in cache
- `--verbose, -v`: Show detailed output including all found strings and their sources
- `--help`: Show help message

### Example Output

```
TTS String Cache Utility
========================================
Scanning Python files for TTS strings...
Found 31 unique TTS strings

Caching 31 TTS strings...

[1/31] Processing: AAH!! How's a hyperintelligent supercomputer supposed to...
  Cached: a143e005f4cbdaa8856c8bc099535596d6b53790d0e9257866cca5c1a7ec14f8.mp3

[2/31] Processing: Aggression, an interesting choice.
  Cached: 3722ec9f199faff1779de28ab1151c67994f081cc36c5fe69a95acf2ffb5c192.mp3

...

Caching complete!
Successfully cached: 31
Errors: 0
Total strings: 31
```

### How It Works

1. **Scanning**: The script recursively scans all Python files in the project directories
2. **Pattern Matching**: Uses multiple regex patterns to identify TTS strings:
   - `SYNTHESIZE_SPEECH` calls with text parameters
   - Speech text constants and variables
   - Button response texts in lambda functions
   - Diagnosis options in data structures
3. **Filtering**: Removes duplicates and filters out non-TTS content
4. **Caching**: Uses the existing `SpeechSynthesizer` class to generate and cache audio files
5. **Deduplication**: Automatically skips strings that are already cached (unless `--force` is used)

### Cache Location

Cached audio files are stored in the directory specified by `TTS_CACHE_DIR` in your settings (typically `assets/tts_cache/`). Each file is named with a SHA-256 hash of the text content and TTS parameters.

### When to Run

- **Initial Setup**: Run once to pre-cache all existing TTS strings
- **After Adding New Content**: Run after adding new scenes or dialogue
- **Before Demos/Releases**: Run to ensure smooth playback performance
- **After TTS Settings Changes**: Run with `--force` if you change voice or model settings

### Troubleshooting

- **No strings found**: Check that your project structure matches the expected directories
- **API errors**: Verify your ElevenLabs API key is valid and has sufficient credits
- **Cache issues**: Use `--force` to regenerate existing cache files
- **Permission errors**: Ensure write permissions to the cache directory

### Performance Notes

- Caching 31 strings typically takes 2-5 minutes depending on API response time
- Each API call uses ElevenLabs credits
- Cached files are reused across sessions to minimize API usage
- Large text strings take longer to synthesize than short ones 