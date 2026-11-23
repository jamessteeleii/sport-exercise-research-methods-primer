"""Trim blank figure margins using SVG viewports, keeping original pixels intact.

Only the manually inspected figure list below is cropped. Each derivative embeds
the unmodified source and a padded viewport; the manifest records the provenance.
"""
from pathlib import Path
import base64, hashlib, json, re
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SELECTED = [1, 4, 10, 12, 42, 44, 45, 46, 47, 48, 49, 50, 60, 70]

def main():
    dest = ROOT / 'assets/figure-crops'
    dest.mkdir(exist_ok=True)
    manifest = []
    for number in SELECTED:
        source = ROOT / f'assets/imported/media/image{number}.png'
        im = Image.open(source).convert('RGBA')
        bg = Image.new('RGBA', im.size, 'white')
        bg.alpha_composite(im)
        difference = ImageChops.difference(bg.convert('RGB'), Image.new('RGB', im.size, 'white'))
        mask = difference.convert('L').point(lambda value: 255 if value > 18 else 0)
        box = mask.getbbox()
        if box is None:
            raise ValueError(f'No figure content: {source}')
        pad = max(12, round(min(im.size) * .02))
        x0, y0, x1, y1 = max(0, box[0]-pad), max(0, box[1]-pad), min(im.width, box[2]+pad), min(im.height, box[3]+pad)
        width, height = x1-x0, y1-y0
        payload = base64.b64encode(source.read_bytes()).decode('ascii')
        output = dest / f'image{number}.svg'
        output.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="{x0} {y0} {width} {height}"><image width="{im.width}" height="{im.height}" xlink:href="data:image/png;base64,{payload}"/></svg>\n', encoding='utf8')
        manifest.append({'source': source.relative_to(ROOT).as_posix(), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'derivative': output.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'viewport': [x0,y0,width,height], 'original_size': list(im.size), 'method': 'SVG viewport; embedded original pixels unchanged; padded white-margin crop'})
        for chapter in (ROOT/'chapters').glob('*.qmd'):
            text = chapter.read_text(encoding='utf8')
            updated = text.replace(f'../assets/imported/media/image{number}.png', f'../assets/figure-crops/image{number}.svg')
            if updated != text:
                chapter.write_text(updated, encoding='utf8')
    (ROOT/'config/figure-crops.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf8')
    print(f'Prepared {len(manifest)} inspected figure margin crops; originals unchanged.')

if __name__ == '__main__':
    main()
