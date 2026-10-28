# Qiita Atlas explorer

An interactive 3D presentation of the Qiita Atlas: 7,236 full-text human-microbiome papers (2010-2026), arranged by text similarity and labeled by body site and MONDO disease (release 2026-09-01). Includes a guided tour; every point links to its paper on PubMed.

The layout is the published 2D map filmed by a moving camera; the third dimension is presentation, not measurement. The embedded data is byte-verified identical to the published atlas (see DATA_PROVENANCE.md).

**Hosting:** two static files, no build step. Vercel: import this repo, no build step, output directory `.`. GitHub Pages: Settings, Pages, deploy from branch `main`, root.

**Local:** open `index.html` in a browser (fonts and Three.js load from CDNs).

License: MIT. Built by Saleem Sabeer with Claude; data from the Qiita Atlas project (S. DeGregori and S. Sabeer).
