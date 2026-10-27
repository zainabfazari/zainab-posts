"""Usage: python3 -I render_any.py <html name in build/> <out dir name> <prefix> [--pdf]
Screenshots every section.slide (by order) to <out>/<prefix>-NN.png; optional PDF for 1350px slides."""
import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

S = Path(__file__).resolve().parent
html, outname, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
want_pdf = "--pdf" in sys.argv
out = S / outname; out.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 2000})
        await pg.goto((S / "build" / html).as_uri())
        await pg.evaluate("document.fonts.ready")
        slides = pg.locator("section.slide")
        n = await slides.count()
        files = []
        for i in range(n):
            f = out / f"{prefix}-{i+1:02d}.png"
            await slides.nth(i).screenshot(path=str(f), omit_background=True)
            files.append(f)
        if want_pdf:
            await pg.add_style_tag(content="@page{size:1080px 1350px;margin:0} body{background:none} .slide{margin:0;page-break-after:always}")
            await pg.pdf(path=str(out / f"{prefix}.pdf"), width="1080px", height="1350px", print_background=True)
        await b.close()
        return files

files = asyncio.run(main())
ims = [Image.open(f) for f in files]
h0 = ims[0].height
scale = 0.4
w, h = int(1080 * scale), int(h0 * scale)
cols = min(len(ims), 5); rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), "#888")
for k, im in enumerate(ims):
    sheet.paste(im.convert("RGB").resize((w, int(im.height * scale))), ((k % cols) * w, (k // cols) * h))
sheet.save(S / f"sheet-{prefix}.png")
print(len(files), "slides")
