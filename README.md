# Music Downloader ⚞^. .^⚟
Automatically downloads music as high-quality MP3 from a plain text list of track titles. The script searches each title on YouTube and downloads the best available audio, with metadata and album art embedded.
Spotify/Youtube playlist option coming soon /•᷅‎‎•᷄\੭

I created this project because I needed to batch download content to train DJing from home :b 

*anyways*

# How to use 𐔌՞ ܸ.ˬ. ܸ՞𐦯

## Requirements

### Python
Python 3.10 or higher

### Python dependencies
```bash
pip install yt-dlp
```

### ffmpeg (required for MP3 conversion)

| OS | Command |
|----|---------|
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |


## Usage
Create a `titles.txt` file in your folder, and type in `artist - title` on separate lines (*more info below*)

### Basic command 💗ྀི
```bash
python music_downloader.py --list titles.txt
```

### With a custom output folder
```bash
python music_downloader.py --list titles.txt --output ./music
```

### With a custom delay between downloads
```bash
python music_downloader.py --list titles.txt --delay 3
```

### All options combined
```bash
python music_downloader.py --list titles.txt --output ~/Music --delay 2
```

## Titles file format

One title per line. The `Artist - Title` format is **strongly recommended** for accurate YouTube search results.

Lines starting with `#` are ignored (comments).

**Example `titles.txt`:**
```
# My favourite tracks

Daft Punk - Touch 
Veridis Project - ça va ensemble II
PLK - ça mène à rien
```

## Where are the files saved?

MP3 files are saved in the folder specified by `--output`.

By default (without `--output`), a `musiques/` folder is created **in the same directory as the script**.

To quickly find the folder after a download:

```bash
# Linux / macOS
ls ./musiques

# Windows
dir musiques
```

**Tip:** avoid paths with spaces or special characters. Prefer `./my_music` over `./My Music` 


## Audio quality

- Format: **MP3**
- Quality: **Maximum VBR** (best audio available on YouTube)
- Metadata (title, artist) automatically embedded
- Album art automatically embedded
- Files that already exist are **not re-downloaded**

## Common issues 🍮🥄 ˚₊‧

**Wrong song downloaded**
The script picks the first YouTube result. For better accuracy, use the `Artist - Title` format rather than just the song title alone.

**Download blocked / slow**
Increase the delay between requests with `--delay 5` to avoid YouTube rate limiting.
