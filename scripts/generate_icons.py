# PWA Icon Generator Script
# This creates placeholder icons for the PWA
# Replace these with actual CELPIP-branded icons

import os
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    """Create a simple placeholder icon"""
    # Create image with gradient-like background
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw simple design
    # Gradient effect (simplified)
    for i in range(size):
        color_value = int(102 + (118 - 102) * (i / size))  # 667eea to 764ba2
        draw.line([(0, i), (size, i)], fill=(color_value, 126, 234))
    
    # Draw text "CP" in center
    try:
        # Try to use a nice font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size * 0.4))
    except:
        # Fallback to default
        font = ImageFont.load_default()
    
    text = "CP"
    # Get text size using textbbox
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) / 2, (size - text_height) / 2)
    draw.text(position, text, fill='white', font=font)
    
    # Save
    img.save(filename, 'PNG')
    print(f"Created: {filename}")

# Create icons directory
os.makedirs('static/icons', exist_ok=True)

# Generate all required sizes
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    create_icon(size, f'static/icons/icon-{size}x{size}.png')

print("\n✅ All icons generated!")
print("📝 Note: Replace these placeholder icons with branded CELPIP icons for production")

