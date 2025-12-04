# Icon Placeholders

These icon files are placeholders for the PWA.

## To Replace with Real Icons:

1. Create your CELPIP-branded icon (square, at least 512x512px)
2. Use an online tool to generate all sizes:
   - https://realfavicongenerator.net/
   - https://www.pwabuilder.com/imageGenerator
   
3. Or use ImageMagick:
   ```bash
   # Install ImageMagick first
   brew install imagemagick
   
   # Generate all sizes from one source image
   for size in 72 96 128 144 152 192 384 512; do
     convert source-icon.png -resize ${size}x${size} icon-${size}x${size}.png
   done
   ```

4. Replace the files in this directory

## Required Sizes:
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png (iOS)
- icon-192x192.png (Android)
- icon-384x384.png
- icon-512x512.png (Android maskable)

## Design Guidelines:
- Square format (1:1 ratio)
- Solid background color
- Clear, simple design
- Recognizable at small sizes
- Brand colors (purple gradient)
- "CELPIP" or "CP" text

