#!/usr/bin/env python3
"""
Organize raw listening audio files from celpip-materials into the
standardized naming convention for Cloudinary upload.

Source structure (celpip-materials-1):
  Test X_/Listening X/
    PART 1 - 1.m4a          (passage: Part 1, Section 1)
    Part 1-2.m4a             (passage: Part 1, Section 2)
    Part 1 - 3.m4a           (passage: Part 1, Section 3)
    PART 2.m4a               (passage: Part 2)
    ...
    PART 5.mp4               (video:   Part 5)
    PART 6.m4a               (passage: Part 6)
    L3-T1-Q1.m4a             (question: Listening 3, Part 1, Q1)
    L3-T2-Q3.m4a             (question: Listening 3, Part 2, Q3)

Target structure:
  organized/test_N/
    p1-1-pas.m4a             (Part 1, Section 1 passage)
    p1-2-pas.m4a             (Part 1, Section 2 passage)
    p1-3-pas.m4a             (Part 1, Section 3 passage)
    p1-q1.m4a                (Part 1, Question 1)
    ...
    p2-pas.m4a               (Part 2 passage)
    p2-q1.m4a                (Part 2, Question 1)
    ...
    p5-pas.mp4               (Part 5 video)
    p6-pas.m4a               (Part 6 passage)

Usage:
  # Dry run — see what would be copied
  python scripts/organize_listening_audio.py --dry-run

  # Copy all files
  python scripts/organize_listening_audio.py

  # Specific tests only
  python scripts/organize_listening_audio.py --tests 3 4 5

  # Custom source and output directories
  python scripts/organize_listening_audio.py --source /path/to/materials --output /path/to/output
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


SOURCE_DIR = "/data/celpip-materials-1"
OUTPUT_DIR = "/data/celpip-materials-1/organized"


def find_listening_dirs(source_dir):
    """
    Find all Test*/Listening* directories and return a dict of {test_num: path}.
    """
    results = {}
    for entry in os.listdir(source_dir):
        full = os.path.join(source_dir, entry)
        if not os.path.isdir(full):
            continue

        match = re.match(r'Test\s+(\d+)', entry, re.IGNORECASE)
        if not match:
            match = re.match(r'Sample\s+([A-Z])', entry, re.IGNORECASE)
        if not match:
            continue

        test_id = match.group(1)

        for sub in os.listdir(full):
            sub_path = os.path.join(full, sub)
            if os.path.isdir(sub_path) and sub.lower().startswith("listening"):
                results[test_id] = sub_path
                break

    return results


def rename_passage_file(filename):
    """
    Convert passage filenames to the standardized format.
    Handles variations: 'PART 1 - 1.m4a', 'Part 1-1.m4a', 'part-6.m4a', etc.
    Returns (new_name, ext) or None if not a passage file.
    """
    name_lower = filename.lower()
    stem = Path(filename).stem
    ext = Path(filename).suffix.lower()

    stem_clean = re.sub(r'\s+', ' ', stem).strip()

    # "Part 1 - 1" / "PART 1 - 2" / "Part 1-3" → p1-{section}-pas
    m = re.match(r'part\s*1\s*[-–]\s*([1-3])', stem_clean, re.IGNORECASE)
    if m:
        section = m.group(1)
        return f"p1-{section}-pas{ext}", ext

    # "part-6" → p6-pas
    m = re.match(r'part\s*[-–]?\s*([2-6])', stem_clean, re.IGNORECASE)
    if m:
        part_num = m.group(1)
        return f"p{part_num}-pas{ext}", ext

    return None


def rename_question_file(filename, listening_num):
    """
    Convert question filenames to the standardized format.
    'L3-T1-Q1.m4a' → 'p1-q1.m4a'
    'L10-T2-Q3.mp3' → 'p2-q3.mp3'
    'LA-T1-Q1.m4a'  → 'p1-q1.m4a' (Sample A)
    Returns (new_name, ext) or None if not a question file.
    """
    stem = Path(filename).stem
    ext = Path(filename).suffix.lower()

    m = re.match(
        r'L([A-Z\d]+)-T(\d+)-Q(\d+)',
        stem,
        re.IGNORECASE
    )
    if not m:
        return None

    file_listening_id = m.group(1).upper()
    part_num = m.group(2)
    question_num = m.group(3)

    listening_id_upper = str(listening_num).upper()

    # Match by listening ID, also accept related IDs for Sample folders
    # Sample A contains L19 and LA files; Sample B contains L20 and LB files
    aliases = {
        'A': {'A', '19'},
        'B': {'B', '20'},
    }
    valid_ids = aliases.get(listening_id_upper, {listening_id_upper})

    if file_listening_id not in valid_ids:
        return None

    return f"p{part_num}-q{question_num}{ext}", ext


def process_test(listening_num, listening_dir, output_dir, dry_run=False):
    """
    Process one test's listening directory.
    Returns list of (src, dst, status) tuples.
    """
    results = []
    dest_dir = os.path.join(output_dir, f"test_{listening_num}")

    audio_exts = {'.m4a', '.mp3', '.mp4', '.ogg', '.wav', '.flac', '.aac', '.webm'}

    files = os.listdir(listening_dir)
    seen_destinations = {}

    for filename in sorted(files):
        src = os.path.join(listening_dir, filename)
        if not os.path.isfile(src):
            continue

        ext = Path(filename).suffix.lower()
        if ext not in audio_exts:
            continue

        new_name = None

        result = rename_passage_file(filename)
        if result:
            new_name, _ = result

        if not new_name:
            result = rename_question_file(filename, listening_num)
            if result:
                new_name, _ = result

        if not new_name:
            results.append((src, None, f"SKIPPED (unrecognized): {filename}"))
            continue

        dst = os.path.join(dest_dir, new_name)

        if new_name in seen_destinations:
            results.append((src, dst, f"DUPLICATE (already mapped from {seen_destinations[new_name]}): {filename} -> {new_name}"))
            continue

        seen_destinations[new_name] = filename

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(src, dst)

        results.append((src, dst, "OK"))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Organize listening audio files into standardized naming for Cloudinary upload",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--source', default=SOURCE_DIR,
        help=f'Source materials directory (default: {SOURCE_DIR})'
    )
    parser.add_argument(
        '--output', default=OUTPUT_DIR,
        help=f'Output directory for organized files (default: {OUTPUT_DIR})'
    )
    parser.add_argument(
        '--tests', nargs='+',
        help='Specific test numbers to process (e.g., --tests 3 4 5). Default: all.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be copied without actually copying'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"ERROR: Source directory not found: {args.source}")
        sys.exit(1)

    listening_dirs = find_listening_dirs(args.source)
    if not listening_dirs:
        print(f"ERROR: No Test*/Listening* directories found in: {args.source}")
        sys.exit(1)

    if args.tests:
        filtered = {}
        for t in args.tests:
            if t in listening_dirs:
                filtered[t] = listening_dirs[t]
            else:
                print(f"WARNING: Test {t} not found (available: {sorted(listening_dirs.keys(), key=lambda x: int(x) if x.isdigit() else x)})")
        listening_dirs = filtered

    if not listening_dirs:
        print("No tests to process.")
        sys.exit(1)

    def sort_key(k):
        try:
            return (0, int(k))
        except ValueError:
            return (1, k)

    sorted_tests = sorted(listening_dirs.keys(), key=sort_key)

    print(f"{'DRY RUN — ' if args.dry_run else ''}Organizing listening audio files")
    print(f"Source:  {args.source}")
    print(f"Output:  {args.output}")
    print(f"Tests:   {', '.join(sorted_tests)}")
    print("=" * 70)

    total_ok = 0
    total_skipped = 0
    total_dup = 0
    empty_tests = []

    for test_id in sorted_tests:
        src_dir = listening_dirs[test_id]
        print(f"\nTest {test_id}: {src_dir}")
        print("-" * 50)

        results = process_test(test_id, src_dir, args.output, dry_run=args.dry_run)

        if not results:
            print("  (no audio/video files found)")
            empty_tests.append(test_id)
            continue

        for src, dst, status in results:
            src_name = os.path.basename(src)
            if status == "OK":
                dst_name = os.path.basename(dst)
                print(f"  {src_name:30s} -> {dst_name}")
                total_ok += 1
            elif status.startswith("SKIPPED"):
                print(f"  {status}")
                total_skipped += 1
            elif status.startswith("DUPLICATE"):
                print(f"  {status}")
                total_dup += 1

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Copied:     {total_ok} files")
    print(f"  Skipped:    {total_skipped} files (unrecognized names)")
    print(f"  Duplicates: {total_dup} files")
    if empty_tests:
        print(f"  Empty tests: {', '.join(empty_tests)} (no audio files)")

    if total_ok > 0 and not args.dry_run:
        print(f"\nOrganized files are in: {args.output}")
        print("\nNext step — upload to Cloudinary:")
        print(f"  python scripts/gdrive_to_cloudinary.py \\")
        print(f"    --local {args.output}/test_N \\")
        print(f"    --cloudinary-folder celpip/test_N/listening")
    elif args.dry_run:
        print("\n(Dry run — no files were copied. Remove --dry-run to copy.)")

    print("\nDone!")


if __name__ == "__main__":
    main()
