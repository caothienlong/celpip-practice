#!/bin/bash

# OCR Script - Convert specific page range from PDF to text
# Usage: ./convert_pages_range.sh START_PAGE END_PAGE OUTPUT_NAME
# Example: ./convert_pages_range.sh 1 35 test1_and_test2

if [ $# -lt 3 ]; then
    echo "Usage: $0 START_PAGE END_PAGE OUTPUT_NAME"
    echo "Example: $0 1 35 test1_and_test2"
    exit 1
fi

PDF_FILE="FULL READING TEST.pdf"
START_PAGE=$1
END_PAGE=$2
OUTPUT_NAME=$3
OUTPUT_FILE="${OUTPUT_NAME}.txt"
TEMP_DIR="temp_ocr_${OUTPUT_NAME}"

echo "🚀 Starting OCR conversion..."
echo "PDF: $PDF_FILE"
echo "Pages: $START_PAGE to $END_PAGE"

# Create temp directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# Step 1: Convert PDF pages to PNG images
echo ""
echo "📄 Converting PDF pages $START_PAGE-$END_PAGE to images..."
pdftocairo -png -f $START_PAGE -l $END_PAGE "../$PDF_FILE" page

# Count generated images
NUM_PAGES=$(ls page-*.png 2>/dev/null | wc -l | tr -d ' ')
echo "✓ Generated $NUM_PAGES images"

# Step 2: OCR each image
echo ""
echo "🔍 Running OCR on all pages..."
> "../$OUTPUT_FILE"  # Create/clear output file

PAGE_NUM=$START_PAGE
for png_file in page-*.png; do
    echo -n "Processing page $PAGE_NUM... "
    
    # Get the image number from filename
    IMG_NUM=$(echo "$png_file" | sed 's/page-\([0-9]*\).png/\1/')
    
    # Run tesseract OCR
    tesseract "$png_file" "output-$IMG_NUM" -l eng 2>/dev/null
    
    # Append to final output
    echo "=== PAGE $PAGE_NUM ===" >> "../$OUTPUT_FILE"
    cat "output-$IMG_NUM.txt" >> "../$OUTPUT_FILE"
    echo "" >> "../$OUTPUT_FILE"  # Add blank line between pages
    
    echo "✓"
    PAGE_NUM=$((PAGE_NUM + 1))
done

# Step 3: Cleanup
echo ""
echo "🧹 Cleaning up temporary files..."
cd ..
rm -rf "$TEMP_DIR"

echo ""
echo "✅ DONE! Output saved to: $OUTPUT_FILE"
echo "📊 Total pages processed: $NUM_PAGES"
echo ""
echo "To view the output:"
echo "  cat $OUTPUT_FILE"
echo "  less $OUTPUT_FILE"

