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

# Endorsement: "A Terrane Geomatics company" is its own link (to /terrane/)
# under the JSA logo, in the header and footer. The logo alone links home.
IMG = '<img class="jsa-logo" src="jsa-logo.svg" alt="Jones Snyder &amp; Associates">'
ENDORSE_LINK = ('<a class="jsa-endorse endorse-link" href="/terrane/">A Terrane Geomatics company'
                '<span class="arr" aria-hidden="true"> →</span></a>')
HOME = '<a class="brand" href="#top" aria-label="Jones Snyder &amp; Associates home">'
s, n = re.subn(
    re.escape(HOME + '<span class="jsa-lockup">' + LOGO) + r'(<em class="tagline">.*?</em>)?</span>\s*</a>',
    lambda m: '<div class="jsa-lockup">' + HOME + IMG + '</a>' + ENDORSE_LINK + (m.group(1) or '') + '</div>',
    s, flags=re.S)
assert n == 2, f"expected header and footer logos, found {n}"
swap("a dba of Terrane Geomatics, Inc.",
     'a dba of <a class="legal-link" href="/terrane/">Terrane Geomatics, Inc.</a>')
swap("</style>", """.jsa-lockup > .brand{display:block;align-self:flex-start}
.jsa-logo{align-self:flex-start}
.endorse-link{text-decoration:none;align-self:flex-start;padding:6px 0;margin:-6px 0;transition:color .2s}
.endorse-link .arr{opacity:0;transition:opacity .2s}
.endorse-link:hover,.endorse-link:focus-visible{color:var(--gold)}
.endorse-link:hover .arr,.endorse-link:focus-visible .arr{opacity:1}
@media (hover:none){.endorse-link .arr{opacity:.7}}
.legal-link{color:inherit;text-decoration:underline;text-decoration-color:rgba(201,160,78,.5);text-underline-offset:3px}
.legal-link:hover{color:var(--gold-hi)}
</style>""")

leftover = [m for m in re.findall(r"[^<>]{0,40}Terrane[^<>]{0,40}", s)
            if "Terrane Geomatics company" not in m and "dba of Terrane" not in m and "/terrane/" not in m and m.strip() != "Terrane Geomatics, Inc."]
if leftover:
    print("Check these Terrane mentions:", *leftover, sep="\n  ")

(root / "jsa").mkdir(exist_ok=True)
(root / "jsa" / "index.html").write_text(s)
print("wrote jsa/index.html")
