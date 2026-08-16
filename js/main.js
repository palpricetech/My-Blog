/* ============================================
   Tech Unplugged — main.js
   Theme toggle + post loading from posts.json
   ============================================ */

// ---------- Theme toggle (light default, remembers choice) ----------
(function initTheme() {
  let saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) { /* storage unavailable */ }
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = saved || (prefersDark ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
})();

function setupThemeToggle() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  const icon = () =>
    document.documentElement.getAttribute("data-theme") === "dark" ? "☀️" : "🌙";
  btn.textContent = icon();
  btn.addEventListener("click", () => {
    const next =
      document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) { /* ignore */ }
    btn.textContent = icon();
  });
}

// ---------- Load posts.json ----------
async function loadPosts() {
  const res = await fetch("posts.json");
  if (!res.ok) throw new Error("Could not load posts.json");
  const posts = await res.json();
  // newest first
  posts.sort((a, b) => new Date(b.date) - new Date(a.date));
  return posts;
}

function postCard(post) {
  const tags = post.tags
    .map((t) => `<span class="tag">#${t}</span>`)
    .join("");
  return `
    <article class="post-card">
      <span class="date">${post.date}</span>
      <h3><a href="post.html?id=${post.slug}">${post.title}</a></h3>
      <p>${post.excerpt}</p>
      <div class="tags">${tags}</div>
    </article>`;
}

// ---------- Homepage: latest 3 posts ----------
async function renderLatest() {
  const el = document.getElementById("latest-posts");
  if (!el) return;
  try {
    const posts = await loadPosts();
    el.innerHTML = posts.slice(0, 3).map(postCard).join("");
  } catch (e) {
    el.innerHTML = `<p>Posts could not be loaded. If you opened this file directly, run a local server: <code>python3 -m http.server</code></p>`;
  }
}

// ---------- Blog page: all posts + tag filter ----------
async function renderBlog() {
  const list = document.getElementById("all-posts");
  const filterBar = document.getElementById("filter-bar");
  if (!list) return;
  try {
    const posts = await loadPosts();
    const tags = [...new Set(posts.flatMap((p) => p.tags))].sort();

    let active = null;
    const draw = () => {
      const shown = active ? posts.filter((p) => p.tags.includes(active)) : posts;
      list.innerHTML = shown.map(postCard).join("") || "<p>No posts yet.</p>";
    };

    if (filterBar) {
      filterBar.innerHTML =
        `<button class="tag" data-tag="" aria-pressed="true">all</button>` +
        tags
          .map((t) => `<button class="tag" data-tag="${t}" aria-pressed="false">#${t}</button>`)
          .join("");
      filterBar.addEventListener("click", (ev) => {
        const btn = ev.target.closest("button.tag");
        if (!btn) return;
        active = btn.dataset.tag || null;
        filterBar
          .querySelectorAll("button.tag")
          .forEach((b) => b.setAttribute("aria-pressed", b === btn ? "true" : "false"));
        draw();
      });
    }
    draw();
  } catch (e) {
    list.innerHTML = `<p>Posts could not be loaded. If you opened this file directly, run a local server: <code>python3 -m http.server</code></p>`;
  }
}

// ---------- Post page: render one markdown file ----------
async function renderPost() {
  const body = document.getElementById("post-body");
  if (!body) return;
  const slug = new URLSearchParams(location.search).get("id");
  if (!slug || !/^[a-z0-9-]+$/.test(slug)) {
    body.innerHTML = "<p>Post not found.</p>";
    return;
  }
  try {
    const posts = await loadPosts();
    const meta = posts.find((p) => p.slug === slug);
    if (!meta) throw new Error("unknown post");

    document.title = meta.title + " — Tech Unplugged";
    document.getElementById("post-title").textContent = meta.title;
    document.getElementById("post-date").textContent = meta.date;
    document.getElementById("post-tags").innerHTML = meta.tags
      .map((t) => `<span class="tag">#${t}</span>`)
      .join(" ");

    const res = await fetch(`posts/${slug}.md`);
    if (!res.ok) throw new Error("markdown missing");
    const md = await res.text();
    body.innerHTML = marked.parse(md);
  } catch (e) {
    body.innerHTML = `<p>This post could not be loaded. If you opened this file directly, run a local server: <code>python3 -m http.server</code></p>`;
  }
}

// ---------- Init ----------
document.addEventListener("DOMContentLoaded", () => {
  setupThemeToggle();
  renderLatest();
  renderBlog();
  renderPost();
});
