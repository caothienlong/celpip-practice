#!/bin/bash

# OCR Script - Convert all PDF pages to text
# Usage: ./convert_all_pages.sh

PDF_FILE="FULL READING TEST.pdf"
OUTPUT_FILE="full_reading_test_ocr.txt"
TEMP_DIR="temp_ocr"

echo "🚀 Starting OCR conversion..."
echo "PDF: $PDF_FILE"

# Create temp directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# Step 1: Convert PDF to PNG images
echo ""
echo "📄 Converting PDF to images..."
pdftocairo -png "../$PDF_FILE" page

# Count generated images
NUM_PAGES=$(ls page-*.png 2>/dev/null | wc -l | tr -d ' ')
echo "✓ Generated $NUM_PAGES images"

# Step 2: OCR each image
echo ""
echo "🔍 Running OCR on all pages..."
> "../$OUTPUT_FILE"  # Create/clear output file

for i in $(seq 1 $NUM_PAGES); do
    echo -n "Processing page $i/$NUM_PAGES... "
    
    # Run tesseract OCR
    tesseract "page-$i.png" "output-$i" -l eng 2>/dev/null
    
    # Append to final output
    cat "output-$i.txt" >> "../$OUTPUT_FILE"
    echo "" >> "../$OUTPUT_FILE"  # Add blank line between pages
    
    echo "✓"
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

