#!/usr/bin/env python3
"""
Migrate audio/video files from Google Drive to Cloudinary.

Supports:
  - Individual Google Drive shared links
  - A Google Drive folder (shared publicly or via link)
  - A local CSV/text file listing Google Drive URLs

Usage:
  # Single file
  python scripts/gdrive_to_cloudinary.py --url "https://drive.google.com/file/d/FILE_ID/view"

  # Multiple files (space-separated)
  python scripts/gdrive_to_cloudinary.py --url "URL1" "URL2" "URL3"

  # All files in a shared Google Drive folder
  python scripts/gdrive_to_cloudinary.py --folder "https://drive.google.com/drive/folders/FOLDER_ID"

  # From a text file (one URL per line)
  python scripts/gdrive_to_cloudinary.py --file urls.txt

  # Upload + update JSON test data (replace placeholder URLs)
  python scripts/gdrive_to_cloudinary.py --folder "FOLDER_URL" --update-json data/test_3/listening

  # Dry run (download only, no Cloudinary upload)
  python scripts/gdrive_to_cloudinary.py --url "URL" --dry-run

  # Specify a Cloudinary folder
  python scripts/gdrive_to_cloudinary.py --url "URL" --cloudinary-folder "celpip/test_3/listening"

Prerequisites:
  pip install cloudinary gdown

Environment variables (in .env or exported):
  CLOUDINARY_CLOUD_NAME=your-cloud-name
  CLOUDINARY_API_KEY=your-api-key
  CLOUDINARY_API_SECRET=your-api-secret
"""

import argparse
import json
import os
import re
import sys
import tempfile
import glob as globmod
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    import gdown
except ImportError:
    print("ERROR: 'gdown' is required. Install with: pip install gdown")
    sys.exit(1)

try:
    import cloudinary
    import cloudinary.uploader
except ImportError:
    print("ERROR: 'cloudinary' is required. Install with: pip install cloudinary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def configure_cloudinary():
    """Configure Cloudinary from environment variables."""
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        print("ERROR: Missing Cloudinary credentials.")
        print("Set these environment variables (in .env or shell):")
        print("  CLOUDINARY_CLOUD_NAME")
        print("  CLOUDINARY_API_KEY")
        print("  CLOUDINARY_API_SECRET")
        sys.exit(1)

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    print(f"Cloudinary configured for cloud: {cloud_name}")


def extract_gdrive_file_id(url):
    """Extract the file ID from various Google Drive URL formats."""
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)',
        r'/open\?id=([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_gdrive_folder_id(url):
    """Extract the folder ID from a Google Drive folder URL."""
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if 'id' in params:
        return params['id'][0]
    return None


def download_from_gdrive(url_or_id, output_dir):
    """Download a file from Google Drive. Returns the local file path."""
    file_id = extract_gdrive_file_id(url_or_id) if '/' in url_or_id else url_or_id
    if not file_id:
        print(f"  WARNING: Could not extract file ID from: {url_or_id}")
        return None

    gdrive_url = f"https://drive.google.com/uc?id={file_id}"
    try:
        output_path = gdown.download(gdrive_url, output=os.path.join(output_dir, ""), fuzzy=True)
        if output_path and os.path.exists(output_path):
            print(f"  Downloaded: {os.path.basename(output_path)} ({os.path.getsize(output_path)} bytes)")
            return output_path
        else:
            print(f"  WARNING: Download failed for file ID: {file_id}")
            return None
    except Exception as e:
        print(f"  ERROR downloading {file_id}: {e}")
        return None


def download_folder_from_gdrive(folder_url, output_dir):
    """Download all files from a Google Drive folder. Returns list of local paths."""
    folder_id = extract_gdrive_folder_id(folder_url)
    if not folder_id:
        print(f"ERROR: Could not extract folder ID from: {folder_url}")
        return []

    gdrive_folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    print(f"Downloading folder: {gdrive_folder_url}")

    try:
        downloaded = gdown.download_folder(
            url=gdrive_folder_url,
            output=output_dir,
            quiet=False,
            remaining_ok=True
        )
        if downloaded:
            paths = [str(p) for p in downloaded if os.path.isfile(str(p))]
            print(f"  Downloaded {len(paths)} files from folder")
            return paths
        else:
            print("  WARNING: No files downloaded from folder.")
            print("  Make sure the folder is shared as 'Anyone with the link'.")
            return []
    except Exception as e:
        print(f"  ERROR downloading folder: {e}")
        return []


def upload_to_cloudinary(local_path, folder=None):
    """Upload a file to Cloudinary. Returns the result dict with secure_url."""
    filename = Path(local_path).stem
    ext = Path(local_path).suffix.lower()

    resource_type = "video"  # Cloudinary uses "video" for both audio and video
    if ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
        resource_type = "image"

    upload_options = {
        "resource_type": resource_type,
        "public_id": filename,
        "overwrite": False,
        "unique_filename": False,
        "use_filename": True,
    }
    if folder:
        upload_options["folder"] = folder

    try:
        result = cloudinary.uploader.upload(local_path, **upload_options)
        print(f"  Uploaded: {result['secure_url']}")
        return result
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"  SKIPPED (already exists): {filename}{ext}")
            cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
            public_id = f"{folder}/{filename}" if folder else filename
            url = f"https://res.cloudinary.com/{cloud_name}/{resource_type}/upload/{public_id}{ext}"
            return {"secure_url": url, "public_id": public_id, "skipped": True}
        print(f"  ERROR uploading {local_path}: {e}")
        return None


def update_json_files(json_dir, url_mapping):
    """
    Update listening JSON files, replacing matching filenames in URLs.

    url_mapping: dict of {filename_stem: cloudinary_url}
    """
    json_files = sorted(globmod.glob(os.path.join(json_dir, "part*.json")))
    if not json_files:
        print(f"  No part*.json files found in {json_dir}")
        return

    updated_count = 0
    for json_path in json_files:
        with open(json_path, 'r') as f:
            content = f.read()

        original = content
        for stem, new_url in url_mapping.items():
            pattern = re.compile(
                r'https?://[^\s"]+/' + re.escape(stem) + r'\.\w+',
                re.IGNORECASE
            )
            content = pattern.sub(new_url, content)

        if content != original:
            with open(json_path, 'w') as f:
                f.write(content)
            print(f"  Updated: {json_path}")
            updated_count += 1

    print(f"  {updated_count} JSON file(s) updated out of {len(json_files)}")


def load_urls_from_file(filepath):
    """Load Google Drive URLs from a text file (one per line)."""
    urls = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls


def print_summary(results):
    """Print a summary table of all uploads."""
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)

    success = [r for r in results if r.get('cloudinary_url')]
    failed = [r for r in results if not r.get('cloudinary_url')]

    if success:
        print(f"\nSuccessfully migrated ({len(success)}):")
        print("-" * 70)
        for r in success:
            status = " (already existed)" if r.get('skipped') else ""
            print(f"  {r['filename']}")
            print(f"    -> {r['cloudinary_url']}{status}")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        print("-" * 70)
        for r in failed:
            print(f"  {r.get('source', 'unknown')}: {r.get('error', 'unknown error')}")

    print(f"\nTotal: {len(success)} succeeded, {len(failed)} failed")
    print("=" * 70)

    if success:
        print("\nCloudinary URLs (copy-paste ready):")
        print("-" * 70)
        for r in success:
            print(r['cloudinary_url'])


def main():
    parser = argparse.ArgumentParser(
        description="Migrate audio/video files from Google Drive to Cloudinary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url "https://drive.google.com/file/d/ABC123/view"
  %(prog)s --folder "https://drive.google.com/drive/folders/XYZ789"
  %(prog)s --file urls.txt --cloudinary-folder celpip/test_3
  %(prog)s --folder "FOLDER_URL" --update-json data/test_3/listening
        """
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '--url', nargs='+',
        help='One or more Google Drive file URLs'
    )
    source_group.add_argument(
        '--folder',
        help='Google Drive shared folder URL'
    )
    source_group.add_argument(
        '--file',
        help='Text file with one Google Drive URL per line'
    )

    parser.add_argument(
        '--cloudinary-folder',
        help='Cloudinary folder to upload into (e.g., "celpip/test_3/listening")'
    )
    parser.add_argument(
        '--update-json',
        help='Path to listening JSON directory to update URLs in (e.g., data/test_3/listening)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Download files but do not upload to Cloudinary'
    )
    parser.add_argument(
        '--keep-downloads', action='store_true',
        help='Keep downloaded files in a local "downloads/" directory instead of temp'
    )

    args = parser.parse_args()

    if not args.dry_run:
        configure_cloudinary()

    if args.keep_downloads:
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)
    else:
        download_dir = tempfile.mkdtemp(prefix="gdrive_migrate_")

    print(f"Download directory: {download_dir}\n")

    local_files = []

    if args.url:
        print(f"Downloading {len(args.url)} file(s) from Google Drive...")
        for url in args.url:
            path = download_from_gdrive(url, download_dir)
            if path:
                local_files.append(path)

    elif args.folder:
        print("Downloading folder from Google Drive...")
        local_files = download_folder_from_gdrive(args.folder, download_dir)

    elif args.file:
        urls = load_urls_from_file(args.file)
        print(f"Downloading {len(urls)} file(s) from URL list...")
        for url in urls:
            path = download_from_gdrive(url, download_dir)
            if path:
                local_files.append(path)

    if not local_files:
        print("\nNo files were downloaded. Nothing to upload.")
        sys.exit(1)

    audio_video_exts = {'.m4a', '.mp3', '.wav', '.ogg', '.flac', '.aac',
                        '.mp4', '.webm', '.mov', '.mkv'}
    media_files = [f for f in local_files
                   if Path(f).suffix.lower() in audio_video_exts]
    non_media = [f for f in local_files if f not in media_files]

    if non_media:
        print(f"\nSkipping {len(non_media)} non-media file(s):")
        for f in non_media:
            print(f"  {os.path.basename(f)}")

    if not media_files:
        print("\nNo audio/video files found to upload.")
        sys.exit(1)

    print(f"\n{'DRY RUN - ' if args.dry_run else ''}Uploading {len(media_files)} file(s) to Cloudinary...\n")

    results = []
    url_mapping = {}

    for filepath in sorted(media_files):
        filename = os.path.basename(filepath)
        stem = Path(filepath).stem
        print(f"Processing: {filename}")

        if args.dry_run:
            print(f"  [DRY RUN] Would upload: {filename}")
            results.append({
                'filename': filename,
                'cloudinary_url': f'[dry-run] {filename}',
                'source': filepath
            })
            continue

        result = upload_to_cloudinary(filepath, folder=args.cloudinary_folder)
        if result:
            results.append({
                'filename': filename,
                'cloudinary_url': result['secure_url'],
                'public_id': result.get('public_id'),
                'skipped': result.get('skipped', False),
                'source': filepath
            })
            url_mapping[stem] = result['secure_url']
        else:
            results.append({
                'filename': filename,
                'cloudinary_url': None,
                'error': 'Upload failed',
                'source': filepath
            })

    print_summary(results)

    if args.update_json and url_mapping and not args.dry_run:
        print(f"\nUpdating JSON files in: {args.update_json}")
        update_json_files(args.update_json, url_mapping)

    if not args.keep_downloads and download_dir.startswith(tempfile.gettempdir()):
        import shutil
        shutil.rmtree(download_dir, ignore_errors=True)
        print(f"\nCleaned up temp downloads.")

    print("\nDone!")


if __name__ == "__main__":
    main()
