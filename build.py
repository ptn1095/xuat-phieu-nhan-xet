"""Đóng gói app thành 1 file index.html chạy độc lập (offline).

Cần: Python 3.9+ với fonttools (pip install fonttools), Node/npm (npm ci).
Chạy: python build.py            -> ghi ra index.html
"""
import base64, io, json, pathlib, sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).parent
FONTS = ROOT / "assets" / "fonts"
IMG = ROOT / "assets" / "img"
NM = ROOT / "node_modules"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index.html"

# Latin + tiếng Việt + dấu câu thông dụng
UNICODES = "U+0020-007E,U+00A0-00FF,U+0100-017F,U+01A0-01B0,U+0300-0323,U+1EA0-1EF9,U+2000-206F,U+20AB,U+2022,U+25CB,U+25E6,U+2190-2193,U+2713"
STYLES = {"Regular": "Regular", "Bold": "Bold", "Italic": "Italic", "BoldItalic": "Bold Italic"}
FAMILY = "PNX Serif"  # Bản cắt gọn phải đổi tên (Reserved Font Name "Liberation", SIL OFL 1.1)


def subset_font(style):
    font = TTFont(FONTS / f"LiberationSerif-{style}.ttf")
    opts = subset.Options()
    opts.layout_features = ["*"]
    opts.drop_tables += ["FFTM"]
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes(UNICODES))
    sub.subset(font)
    sty = STYLES[style]
    full = f"{FAMILY} {sty}" if style != "Regular" else FAMILY
    ps = f"PNXSerif-{style}"
    for rec in font["name"].names:
        if rec.nameID in (1, 16): rec.string = FAMILY
        elif rec.nameID in (2, 17): rec.string = sty
        elif rec.nameID == 3: rec.string = f"{ps};subset"
        elif rec.nameID == 4: rec.string = full
        elif rec.nameID == 6: rec.string = ps
    buf = io.BytesIO(); font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def b64(p): return base64.b64encode(p.read_bytes()).decode()


def lib(p):
    s = (NM / p).read_text(encoding="utf8").replace("</script", "<\\/script")
    return "<script>" + s + "</script>"


assets = {
    "fonts": {f"LS-{s}.ttf": subset_font(s) for s in STYLES},
    "img": {k: "data:image/png;base64," + b64(IMG / f"{k}.png") for k in ("header", "footer", "logo")},
}
libs = "\n".join([
    lib("xlsx/dist/xlsx.full.min.js"),
    lib("jszip/dist/jszip.min.js"),
    lib("pdfmake/build/pdfmake.min.js"),
    "<script>window.ASSETS=" + json.dumps(assets) + ";</script>",
])
src = (ROOT / "src" / "app.src.html").read_text(encoding="utf8")
assert "<!--LIBS-->" in src
OUT.write_text(src.replace("<!--LIBS-->", libs), encoding="utf8")
print(f"Đã ghi {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")
