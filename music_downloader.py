#!/usr/bin/env python3
"""
music_downloader.py
--------------------
Télécharge automatiquement des musiques en MP3 (meilleure qualité)
à partir d'une liste de titres dans un fichier .txt.

Dépendances :
    pip install yt-dlp

    ffmpeg requis pour la conversion MP3 :
      - Windows : https://ffmpeg.org/download.html
      - Linux   : sudo apt install ffmpeg
      - macOS   : brew install ffmpeg

Utilisation :
    python music_downloader.py --list titres.txt
    python music_downloader.py --list titres.txt --output ~/Musique
    python music_downloader.py --list titres.txt --delay 3
"""

import argparse
import sys
import time
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("❌ yt-dlp non installé. Lance : pip install yt-dlp")


# ─── Couleurs terminal ────────────────────────────────────────────────────────
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
CYAN    = "\033[96m"
RESET   = "\033[0m"
BOLD    = "\033[1m"


def search_and_download(query: str, output_dir: Path) -> bool:
    """
    Cherche 'query' directement sur YouTube via yt-dlp (ytsearch1:)
    puis télécharge et convertit en MP3.
    """
    search_query = f"ytsearch1:{query} audio officiel"

    found_title = {}

    class QuietLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg):
            print(f"  {RED}✗ {msg}{RESET}")

    def progress_hook(d):
        if d["status"] == "downloading" and not found_title.get("shown"):
            title    = d.get("info_dict", {}).get("title", "")
            duration = d.get("info_dict", {}).get("duration_string", "??")
            if title:
                print(f"  {CYAN}▶ Trouvé  :{RESET} {title} [{duration}]")
                print(f"  {CYAN}⬇ Téléchargement...{RESET}")
            found_title["shown"] = True

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(artist)s - %(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",   # VBR qualité max
            },
            {
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "writethumbnail": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "nooverwrites": True,
        "logger": QuietLogger(),
        "progress_hooks": [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"  {RED}✗ Erreur : {e}{RESET}")
        return False
    except Exception as e:
        print(f"  {RED}✗ Erreur inattendue : {e}{RESET}")
        return False


def load_titles(filepath: str) -> list[str]:
    """Lit le fichier de titres (1 par ligne, # pour commenter)."""
    path = Path(filepath)
    if not path.exists():
        sys.exit(f"❌ Fichier introuvable : {filepath}")

    titles = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                titles.append(line)

    if not titles:
        sys.exit("❌ Aucun titre trouvé dans le fichier.")
    return titles


def main():
    parser = argparse.ArgumentParser(
        description="Télécharge des musiques YouTube en MP3 depuis un fichier de titres."
    )
    parser.add_argument(
        "--list", "-l",
        required=True,
        metavar="FICHIER.TXT",
        help="Fichier texte contenant les titres (1 par ligne)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./musiques",
        metavar="DOSSIER",
        help="Dossier de sortie (défaut : ./musiques)"
    )
    parser.add_argument(
        "--delay", "-d",
        type=float,
        default=2.0,
        metavar="SECONDES",
        help="Délai entre chaque téléchargement en secondes (défaut : 2)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    titles = load_titles(args.list)
    total  = len(titles)

    print(f"\n{BOLD}🎵 Music Downloader{RESET}")
    print(f"  {total} titre(s) → {output_dir.resolve()}")
    print(f"  💡 Format conseillé : \"Artiste - Titre\" pour de meilleurs résultats")
    print("\n" + "─" * 50)

    success = 0
    failed  = 0

    for i, title in enumerate(titles, 1):
        print(f"\n[{i}/{total}] {BOLD}{title}{RESET}")

        ok = search_and_download(title, output_dir)

        if ok:
            print(f"  {GREEN}✓ OK{RESET}")
            success += 1
        else:
            failed += 1

        if i < total:
            time.sleep(args.delay)

    # ─── Résumé ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 50)
    print(f"{BOLD}📊 Résumé{RESET}")
    print(f"  {GREEN}✓ Succès : {success}{RESET}")
    print(f"  {RED}✗ Échecs : {failed}{RESET}")
    print(f"  📁 Dossier : {output_dir.resolve()}\n")


if __name__ == "__main__":
    main()