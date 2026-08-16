# Tech Unplugged — portfolio + blog

Plain HTML/CSS/JS site. No build step, no framework. Hosted free on GitHub Pages.

## Publish Word posts

Add the Word source as `posts-docx/<slug>.docx` and keep its metadata in
`posts.json`. On every push to `main`, the GitHub Actions workflow converts the
DOCX into the existing Markdown post format and extracts its images into the
deployment artifact. Existing `posts/*.md` files continue to work until a
same-slug DOCX replaces them.

Edit the DOCX, not the generated output; the workflow commits the generated
Markdown and images to `main`, which GitHub Pages publishes as usual. Word page
layout is not copied, so posts retain the site's typography and responsive image styling.

## Deploy to GitHub Pages (one-time setup)

1. Create a new repository on GitHub named `YOUR_USERNAME.github.io`
   (this makes your site live at `https://YOUR_USERNAME.github.io`).
2. In this folder, run:

   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git
   git push -u origin main
   ```

3. On GitHub: repo → **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main`, folder `/ (root)` → Save.
4. Wait a minute or two. Your site is live.

## Legacy Markdown posts

Markdown files in `posts/` still deploy unchanged when no same-slug DOCX exists.
2. Add one entry to `posts.json` (put it anywhere in the list — sorting is by date):

   ```json
   {
     "slug": "docker-basics",
     "title": "Docker Basics",
     "date": "2026-07-15",
     "tags": ["docker", "containers"],
     "excerpt": "One-line summary shown on the post card."
   }
   ```

   The `slug` must match the markdown filename (without `.md`), lowercase with hyphens only.

3. Push:

   ```bash
   git add posts/docker-basics.md posts.json
   git commit -m "New post: Docker Basics"
   git push
   ```

   That's it — live in about a minute. No HTML edits ever needed.

## Preview locally

Because posts are loaded with `fetch()`, opening `index.html` directly from disk won't load them.
Run a tiny local server instead:

```bash
cd this-folder
python3 -m http.server 8000
# open http://localhost:8000
```

## Before you go live — TODO checklist

- [ ] Replace `YOUR_USERNAME` links in `index.html` (footer + project cards)
- [ ] Replace the placeholder projects in `index.html` with your real ones
- [ ] Personalize the About paragraph in `index.html`
- [ ] Complete the 5 migrated posts in `posts/` — each has a `<!-- TODO -->` marker
      where content was truncated; copy the rest from your Blogger posts
- [ ] Optional: add a custom domain in Settings → Pages

## Structure

```
index.html      → homepage (hero, latest posts, projects, about)
blog.html       → all posts with tag filters
post.html       → renders a single post from its markdown file
posts.json      → the post index (title, date, tags, excerpt, slug)
posts/*.md      → one markdown file per post
css/style.css   → light theme + dark mode ([data-theme="dark"])
js/main.js      → theme toggle, post loading, markdown rendering
```
