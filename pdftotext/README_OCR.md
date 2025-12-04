# OCR Conversion Scripts

## 📋 Available Scripts

### 1. Convert ALL Pages (209 pages)
```bash
cd pdftotext
./convert_all_pages.sh
```

**Output:** `full_reading_test_ocr.txt`  
**Time:** ~30-60 minutes (depending on your CPU)

---

### 2. Convert Specific Page Range (RECOMMENDED)
```bash
cd pdftotext
./convert_pages_range.sh START_PAGE END_PAGE OUTPUT_NAME
```

**Examples:**
```bash
# Test 1 (pages 1-17)
./convert_pages_range.sh 1 17 test1

# Test 2 (pages 18-35)
./convert_pages_range.sh 18 35 test2

# Test 3 (estimated pages 36-52)
./convert_pages_range.sh 36 52 test3

# Test 4 (estimated pages 53-69)
./convert_pages_range.sh 53 69 test4

# Test 5 (estimated pages 70-86)
./convert_pages_range.sh 70 86 test5
```

---

## 🎯 Quick Start - Convert Test 1

```bash
cd pdftotext
./convert_pages_range.sh 1 17 test1
cat test1.txt
```

---

## 📊 Estimated Page Numbers

Based on typical CELPIP structure (each test ~17 pages):

| Test | Pages | Command |
|------|-------|---------|
| Test 1 | 1-17 | `./convert_pages_range.sh 1 17 test1` |
| Test 2 | 18-35 | `./convert_pages_range.sh 18 35 test2` |
| Test 3 | 36-52 | `./convert_pages_range.sh 36 52 test3` |
| Test 4 | 53-69 | `./convert_pages_range.sh 53 69 test4` |
| Test 5 | 70-86 | `./convert_pages_range.sh 70 86 test5` |

⚠️ **Note:** Page numbers are estimated. Adjust based on actual PDF structure.

---

## 🔧 Manual Commands

If you prefer to do it manually:

```bash
# Convert specific pages to images
pdftocairo -png -f 1 -l 17 "FULL READING TEST.pdf" page

# OCR a single image
tesseract page-1.png output1 -l eng

# View result
cat output1.txt
```

---

## 📝 Output Files

After running the scripts, you'll find:

- `full_reading_test_ocr.txt` - All 209 pages (if using convert_all_pages.sh)
- `test1.txt`, `test2.txt`, etc. - Individual test sections
- `temp_ocr_*/` - Temporary folders (auto-cleaned)

---

## 🚀 Next Steps After Conversion

1. **Review the OCR output:**
   ```bash
   less test1.txt
   ```

2. **Clean up the text:** Remove headers, page numbers, etc.
   ```bash
   grep -v "Biên soạn\|Compiled by" test1.txt > test1_clean.txt
   ```

3. **Fill in JSON files:** Use the cleaned text to populate the JSON templates

---

## ⚡ Performance Tips

- **Converting all 209 pages takes time!** Use page ranges instead
- Each page takes ~5-10 seconds to process
- Run in background: `./convert_all_pages.sh &`
- Check progress: `tail -f full_reading_test_ocr.txt`

---

## 🐛 Troubleshooting

**Error: `pdftocairo: command not found`**
```bash
brew install poppler
```

**Error: `tesseract: command not found`**
```bash
brew install tesseract
```

**Images not being generated:**
- Check PDF file name: `"FULL READING TEST.pdf"`
- Run from `pdftotext/` directory

**OCR output is garbled:**
- Image quality might be poor
- Try adjusting DPI: `pdftocairo -png -r 300 ...`

