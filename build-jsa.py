"""Build the Jones Snyder & Associates version of the site from index.html.

The Terrane site (index.html) is the master copy. Run this after any change to it:

    python3 build-jsa.py

It writes jsa/index.html: the same page with the JSA logo, JSA contact email
and JSA legal line. Edit the swaps below if the branding changes.
"""
import re
from pathlib import Path

root = Path(__file__).parent
s = (root / "index.html").read_text()

LOGO = (
    '<img class="jsa-logo" src="jsa-logo.svg" alt="Jones Snyder &amp; Associates">'
    '<span class="jsa-endorse">A Terrane Geomatics company</span>'
)


def swap(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"expected {count} of {old[:60]!r}, found {n}"
    s = s.replace(old, new)


# Page title and description
s = re.sub(r"<title>.*?</title>",
           "<title>Jones Snyder &amp; Associates | Land Surveying &amp; Mapping, Oakhurst CA</title>", s, count=1)
s = s.replace('content="Terrane Geomatics: land surveying', 'content="Jones Snyder &amp; Associates: land surveying', 1)

# Image paths: the page lives one folder down
s = s.replace('src="img/', 'src="../img/').replace("url(img/", "url(../img/").replace("url('img/", "url('../img/")

# Header and footer logos
s = re.sub(
    r'(<a class="brand" href="#top" aria-label=")Terrane Geomatics home(">)\s*<svg.*?</svg>\s*<span class="name"><b>TERRANE</b><small>Geomatics</small></span>',
    r'\1Jones Snyder &amp; Associates home\2<span class="jsa-lockup">' + LOGO + '</span>',
    s, count=1, flags=re.S)
s = re.sub(
    r'(<a class="brand" href="#top" aria-label=")Terrane Geomatics home(">)\s*<svg.*?</svg>\s*<span class="name"><b>TERRANE</b><small>Geomatics</small>(<em class="tagline">.*?</em>)</span>',
    r'\1Jones Snyder &amp; Associates home\2<span class="jsa-lockup">' + LOGO + r'\3</span>',
    s, count=1, flags=re.S)
assert "<b>TERRANE</b>" not in s, "a Terrane logo was not replaced"

# Contact email
s = s.replace("info@terrane.land", "nick@jssurveying.com")

# Legal line
s = re.sub(r"<span>© 2026 Terrane Geomatics, Inc\..*?</span>",
           "<span>© 2026 Jones Snyder &amp; Associates, a dba of Terrane Geomatics, Inc.</span>", s, count=1)

# Logo styles
swap("</style>", """.jsa-lockup{display:flex;flex-direction:column;gap:7px}
.jsa-logo{height:44px;width:auto;display:block}
.jsa-endorse{font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:#9FB0C9;line-height:1}
.jsa-lockup .tagline{margin-top:4px}
@media (max-width:420px){.jsa-logo{height:36px}.jsa-endorse{font-size:8.5px}}
</style>""")

leftover = [m for m in re.findall(r"[^<>]{0,40}Terrane[^<>]{0,40}", s)
            if "Terrane Geomatics company" not in m and "dba of Terrane" not in m]
if leftover:
    print("Check these Terrane mentions:", *leftover, sep="\n  ")

(root / "jsa").mkdir(exist_ok=True)
(root / "jsa" / "index.html").write_text(s)
print("wrote jsa/index.html")
