# Embedding the Qiita Atlas in another site

The atlas is static files with only relative asset references, so it can be
dropped into any subdirectory of an existing site unchanged:

```
your-site/
  atlas/
    index.html
    atlas-data.js
    og-image.png
    associations.js   (optional; see SCHEMA.md)
```

…and linked directly at `/atlas/`.

## As an iframe

```html
<iframe src="/atlas/" style="width:100%;height:700px;border:0" title="Qiita Atlas"></iframe>
```

Notes:

- Everything works inside the frame: orbit, stains, the flyover, the tour,
  share links. Keyboard shortcuts (Space, arrows, G, H, Esc) bind to the
  frame, so they work once the visitor has clicked inside it.
- "Share this view" copies a URL to wherever the atlas is being served
  (the iframe's own URL, hash included). If you want shared links to open
  the *host* page instead, link visitors to `/atlas/#...` directly rather
  than framing it, or pass the hash through from the host page.
- The page sets its own Open Graph tags; when embedding, the host page's
  tags win for the host URL, which is usually what you want.
- Give the frame at least ~360px of width; below that the control panel
  auto-collapses, which still works but is less inviting as a first view.
