import os
from PIL import Image, ImageDraw, ImageFont

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')

os.makedirs(CACHE_DIR, exist_ok=True)

def generate_summary_image(total, top5, timestamp):
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype('DejaVuSans-Bold.ttf', 36)
        text_font = ImageFont.truetype('DejaVuSans.ttf', 20)
    except Exception:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    draw.text((40, 30), "Countries Summary", font=title_font, fill=(10, 10, 10))
    draw.text((40, 80), f'Total Countries: {total}', font=text_font, fill=(0, 0, 0))
    draw.text((40, 110), f'Last Refresh: {timestamp.isoformat()}', font=text_font, fill=(0, 0, 0))

    y = 220
    for i, c in enumerate(top5, start=1):
        line = f'{i}. {c["name"]}: {c["estimated_gdp"]:,.2f}' if c["estimated_gdp"] is not None else (f'{i}. '
                                                                                                      f'{c["name"]}: '
                                                                                                      f'N/A')
        draw.text((60, y), line, font=text_font, fill=(0, 0, 0))
        y += 34

    out_path = os.path.join(CACHE_DIR, 'summary.png')
    img.save(out_path)
    return out_path
