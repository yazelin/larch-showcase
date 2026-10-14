// Larch Showcase Dashboard Application

let allWorks = [];
let pingResults = [];
let activeTag = 'ALL';
let searchQuery = '';
let currentSort = 'views-desc';

// DOM Elements
const syncTimeEl = document.getElementById('sync-time');
const kpiViewsEl = document.getElementById('kpi-views');
const kpiPlaysEl = document.getElementById('kpi-plays');
const kpiLikesEl = document.getElementById('kpi-likes');
const kpiCommentsEl = document.getElementById('kpi-comments');
const kpiWorksEl = document.getElementById('kpi-works');
const kpiDeltaViewsEl = document.getElementById('kpi-delta-views');
const kpiDeltaPlaysEl = document.getElementById('kpi-delta-plays');
const kpiDeltaLikesEl = document.getElementById('kpi-delta-likes');
const kpiUnansweredBadgeEl = document.getElementById('kpi-unanswered-badge');
const kpiTotalNodesEl = document.getElementById('kpi-total-nodes');

const worksGridEl = document.getElementById('works-grid');
const tagsContainerEl = document.getElementById('tags-container');
const moreTagsPanelEl = document.getElementById('more-tags-panel');
let isMoreTagsExpanded = false;
const searchInputEl = document.getElementById('search-input');
const sortSelectEl = document.getElementById('sort-select');
const filteredCountEl = document.getElementById('filtered-count');

// Modals
const chapterModalEl = document.getElementById('chapter-modal');
const chapterModalContentEl = document.getElementById('chapter-modal-content');
const closeModalBtn = document.getElementById('close-modal-btn');
const modalTitleEl = document.getElementById('modal-title');
const modalSubtitleEl = document.getElementById('modal-subtitle');
const modalChaptersListEl = document.getElementById('modal-chapters-list');
const modalPlayLinkEl = document.getElementById('modal-play-link');

const pingModalEl = document.getElementById('ping-modal');
const pingModalBtn = document.getElementById('ping-modal-btn');
const closePingModalBtn = document.getElementById('close-ping-modal-btn');
const pingListContainerEl = document.getElementById('ping-list-container');

// Theme Switcher
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIconSun = document.getElementById('theme-icon-sun');
const themeIconMoon = document.getElementById('theme-icon-moon');

function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'light' || (!savedTheme && !prefersDark)) {
    document.documentElement.classList.remove('dark');
    themeIconSun.classList.remove('hidden');
    themeIconMoon.classList.add('hidden');
  } else {
    document.documentElement.classList.add('dark');
    themeIconSun.classList.add('hidden');
    themeIconMoon.classList.remove('hidden');
  }
}

themeToggleBtn.addEventListener('click', () => {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  themeIconSun.classList.toggle('hidden', isDark);
  themeIconMoon.classList.toggle('hidden', !isDark);
});

// Format numbers with commas
function formatNumber(num) {
  return (num || 0).toLocaleString();
}

// Format relative date
function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// Extract external link from description
function extractLinkFromDesc(desc) {
  if (!desc) return null;
  const match = desc.match(/https?:\/\/[^\s\)\n]+/);
  if (match) {
    const url = match[0];
    if (url.includes('github.io') || url.includes('github.com')) {
      return url;
    }
  }
  return null;
}

// Load Data with auto-retry and cache-busting
async function loadData(retryCount = 2) {
  try {
    // Add timestamp to bypass browser cache
    const res = await fetch(`data/works.json?_t=${Date.now()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status} (${res.statusText || '檔案讀取失敗'})`);
    const data = await res.json();
    
    allWorks = data.works || [];
    pingResults = data.ping_results || [];
    
    // Update Header & KPIs
    updateKPIs(data);
    
    // Render Tags
    renderTags();
    
    // Render Works
    applyFiltersAndRender();
  } catch (err) {
    if (retryCount > 0) {
      console.warn(`Fetch data/works.json failed, retrying in 800ms (${retryCount} left)...`, err);
      setTimeout(() => loadData(retryCount - 1), 800);
      return;
    }
    console.error('Failed to load works.json:', err);
    worksGridEl.innerHTML = `
      <div class="col-span-full py-16 text-center text-rose-500">
        <p class="text-base font-bold">載入作品資料失敗</p>
        <p class="text-xs text-slate-400 mt-2">${err.message || '請確認 data/works.json 是否已生成，或 GitHub Action 是否已執行。'}</p>
        <button onclick="loadData()" class="mt-4 px-4 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white text-xs font-semibold transition shadow-sm">
          點此重新載入
        </button>
      </div>
    `;
  }
}

// Update KPI Cards
function updateKPIs(data) {
  const s = data.summary || {};
  const d = data.delta || {};
  
  if (syncTimeEl) {
    syncTimeEl.textContent = data.updated_at_cst || data.updated_at || '剛剛';
  }
  
  kpiViewsEl.textContent = formatNumber(s.total_views);
  kpiPlaysEl.textContent = formatNumber(s.total_plays);
  kpiLikesEl.textContent = formatNumber(s.total_likes);
  kpiCommentsEl.textContent = formatNumber(s.total_comments);
  kpiWorksEl.textContent = formatNumber(s.total_works);
  
  if (d.views > 0) {
    kpiDeltaViewsEl.textContent = `+${formatNumber(d.views)} 今日`;
    kpiDeltaViewsEl.classList.remove('hidden');
  } else {
    kpiDeltaViewsEl.textContent = `持平`;
  }
  
  if (d.plays > 0) {
    kpiDeltaPlaysEl.textContent = `+${formatNumber(d.plays)} 今日`;
  } else {
    kpiDeltaPlaysEl.textContent = `持平`;
  }
  
  if (d.likes > 0) {
    kpiDeltaLikesEl.textContent = `+${formatNumber(d.likes)} 今日`;
  } else {
    kpiDeltaLikesEl.textContent = `持平`;
  }
  
  if (s.total_unanswered > 0) {
    kpiUnansweredBadgeEl.textContent = `待覆 ${s.total_unanswered}`;
    kpiUnansweredBadgeEl.classList.remove('hidden');
  } else {
    kpiUnansweredBadgeEl.classList.add('hidden');
  }
  
  if (kpiTotalNodesEl) {
    kpiTotalNodesEl.textContent = `${formatNumber(s.total_nodes)} 節點`;
  }
}

// Render Tags
function renderTags() {
  const tagCounts = { ALL: allWorks.length };
  allWorks.forEach(w => {
    (w.tags || []).forEach(t => {
      tagCounts[t] = (tagCounts[t] || 0) + 1;
    });
  });
  
  // Top featured categories to display on the primary row
  const FEATURED_CANDIDATES = [
    'ALL',
    '視覺小說',
    '多結局',
    '全語音',
    'RPG',
    '三國改編',
    '第三屆創作者挑戰',
    '第二屆創作者挑戰',
    '背包解謎',
    '專屬配樂',
    '小遊戲'
  ];

  const featuredTags = FEATURED_CANDIDATES.filter(t => t === 'ALL' || (tagCounts[t] && tagCounts[t] > 0));
  
  const allOtherTags = Object.keys(tagCounts)
    .filter(t => !featuredTags.includes(t))
    .sort((a, b) => tagCounts[b] - tagCounts[a]);

  const isSecondaryActive = allOtherTags.includes(activeTag);

  // 1. Render Featured Main Row
  let mainHtml = featuredTags.map(tag => {
    const isSelected = activeTag === tag;
    const label = tag === 'ALL' ? '全部作品' : tag;
    const count = tagCounts[tag] || 0;
    
    return `
      <button 
        data-tag="${tag}"
        class="tag-btn text-xs px-3 py-1.5 rounded-xl font-medium transition flex items-center gap-1.5 ${
          isSelected 
            ? 'bg-brand-500 text-white shadow-sm shadow-brand-500/30' 
            : 'bg-white/70 dark:bg-slate-800/70 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700/80 border border-slate-200/60 dark:border-slate-700/60'
        }"
      >
        <span>${label}</span>
        <span class="text-[10px] px-1.5 py-0.2 rounded-full ${isSelected ? 'bg-white/20' : 'bg-slate-200/60 dark:bg-slate-700'}">${count}</span>
      </button>
    `;
  }).join('');

  // 2. Add "More Tags" toggle button
  if (allOtherTags.length > 0) {
    mainHtml += `
      <button 
        id="toggle-more-tags-btn"
        class="text-xs px-3 py-1.5 rounded-xl font-medium transition flex items-center gap-1.5 ${
          isSecondaryActive 
            ? 'bg-brand-500/15 text-brand-600 dark:text-brand-400 border border-brand-500/40 font-bold' 
            : 'bg-slate-100/90 dark:bg-slate-800/80 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 border border-transparent'
        }"
      >
        <span>${isSecondaryActive ? `已選標籤：${activeTag}` : '更多標籤'}</span>
        <span class="text-[10px] font-mono px-1.5 py-0.2 rounded-full ${isSecondaryActive ? 'bg-brand-500/20 text-brand-600 dark:text-brand-400' : 'bg-black/5 dark:bg-white/10'}">${allOtherTags.length}</span>
        <svg class="w-3.5 h-3.5 transition-transform duration-200 ${isMoreTagsExpanded ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    `;
  }

  tagsContainerEl.innerHTML = mainHtml;

  // 3. Render Secondary Drawer Panel
  if (moreTagsPanelEl) {
    if (isMoreTagsExpanded) {
      moreTagsPanelEl.classList.remove('hidden');
      moreTagsPanelEl.innerHTML = `
        <div class="w-full flex items-center justify-between pb-1.5 text-[11px] font-semibold text-slate-400 dark:text-slate-500">
          <span>進階細部標籤 (${allOtherTags.length})</span>
          <button id="close-more-tags-btn" class="hover:text-slate-600 dark:hover:text-slate-300 font-medium">收起 ✕</button>
        </div>
        ${allOtherTags.map(tag => {
          const isSelected = activeTag === tag;
          const count = tagCounts[tag];
          return `
            <button 
              data-tag="${tag}"
              class="tag-btn text-xs px-2.5 py-1 rounded-lg font-medium transition flex items-center gap-1.5 ${
                isSelected 
                  ? 'bg-brand-500 text-white shadow-sm shadow-brand-500/30' 
                  : 'bg-white dark:bg-surface-900 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200/80 dark:border-slate-700/80'
              }"
            >
              <span>${tag}</span>
              <span class="text-[10px] px-1 rounded-full ${isSelected ? 'bg-white/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'}">${count}</span>
            </button>
          `;
        }).join('')}
      `;

      const closeBtn = document.getElementById('close-more-tags-btn');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          isMoreTagsExpanded = false;
          renderTags();
        });
      }
    } else {
      moreTagsPanelEl.classList.add('hidden');
      moreTagsPanelEl.innerHTML = '';
    }
  }

  // Bind click listeners for tag buttons in main container
  tagsContainerEl.querySelectorAll('.tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeTag = btn.dataset.tag;
      renderTags();
      applyFiltersAndRender();
    });
  });

  // Bind click listeners for tag buttons in more panel
  if (moreTagsPanelEl) {
    moreTagsPanelEl.querySelectorAll('.tag-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        activeTag = btn.dataset.tag;
        renderTags();
        applyFiltersAndRender();
      });
    });
  }

  // Bind toggle more tags button
  const toggleBtn = document.getElementById('toggle-more-tags-btn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      isMoreTagsExpanded = !isMoreTagsExpanded;
      renderTags();
    });
  }
}

// Filter and Sort
function applyFiltersAndRender() {
  let filtered = allWorks.filter(w => {
    // Tag filter
    if (activeTag !== 'ALL') {
      const hasTag = (w.tags || []).includes(activeTag);
      const hasEvent = w.eventId === activeTag;
      if (!hasTag && !hasEvent) return false;
    }
    
    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      const title = (w.title || '').toLowerCase();
      const desc = (w.description || '').toLowerCase();
      const slug = (w.customSlug || '').toLowerCase();
      const tags = (w.tags || []).join(' ').toLowerCase();
      if (!title.includes(q) && !desc.includes(q) && !slug.includes(q) && !tags.includes(q)) {
        return false;
      }
    }
    
    return true;
  });
  
  // Sort
  filtered.sort((a, b) => {
    switch (currentSort) {
      case 'market-rank-asc':
        return (a.marketRank || 999) - (b.marketRank || 999);
      case 'views-desc':
        return (b.views || 0) - (a.views || 0);
      case 'plays-desc':
        return (b.plays || 0) - (a.plays || 0);
      case 'likes-desc':
        return (b.likes || 0) - (a.likes || 0);
      case 'comments-desc':
        return (b.comments || 0) - (a.comments || 0);
      case 'published-desc':
        return new Date(b.publishedAt || 0) - new Date(a.publishedAt || 0);
      case 'updated-desc':
        return new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0);
      default:
        return 0;
    }
  });
  
  filteredCountEl.textContent = filtered.length;
  renderWorks(filtered);
}

// Render Work Cards
function renderWorks(works) {
  if (works.length === 0) {
    worksGridEl.innerHTML = `
      <div class="col-span-full py-16 text-center text-slate-400">
        <svg class="w-12 h-12 mx-auto text-slate-300 dark:text-slate-600 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-sm font-semibold">沒有符合搜尋條件的作品</p>
        <p class="text-xs text-slate-400 mt-1">請嘗試變更關鍵字或標籤篩選</p>
      </div>
    `;
    return;
  }
  
  worksGridEl.innerHTML = works.map(w => {
    const author = w.authorHandle || 'yaze';
    const slug = w.customSlug || w.id;
    const playUrl = w.playUrl || (w.customSlug ? `https://larch.ink/play/market/${author}/${w.customSlug}` : `https://larch.ink/play/market/${w.id}`);
    const workUrl = w.workUrl || (w.customSlug ? `https://larch.ink/work/${w.customSlug}` : `https://larch.ink/work/${w.id}`);
    const coverUrl = w.coverUrl || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&auto=format&fit=crop&q=80';
    
    // AI Disclosure Badge
    let aiBadge = '';
    if (w.aiDisclosure) {
      if (w.aiDisclosure.mode === 'heavy') {
        aiBadge = `<span class="badge-ai-heavy text-[10px] font-semibold px-2 py-0.5 rounded-full">重度 AI</span>`;
      } else if (w.aiDisclosure.mode === 'parts') {
        aiBadge = `<span class="badge-ai-parts text-[10px] font-semibold px-2 py-0.5 rounded-full">局部 AI</span>`;
      } else if (w.aiDisclosure.mode === 'original') {
        aiBadge = `<span class="badge-ai-original text-[10px] font-semibold px-2 py-0.5 rounded-full">原創無 AI</span>`;
      }
    }

    // Event Badge (Clean Chinese Label)
    let eventBadge = '';
    if (w.eventId) {
      const eventNameMap = {
        'creator-challenge-2026-10': '第 3 屆挑戰',
        'creator-challenge-2026-09': '第 2 屆挑戰',
        'creator-challenge-2026-08': '七日挑戰'
      };
      const label = eventNameMap[w.eventId] || w.eventId;
      eventBadge = `<span class="px-2 py-0.5 rounded-full bg-indigo-600/80 backdrop-blur-md text-[10px] font-bold text-white border border-indigo-300/30 shadow-sm">${label}</span>`;
    }

    // Market Rank Badge
    let rankBadge = '';
    if (w.marketRank === 1) {
      rankBadge = `<span class="badge-rank-gold px-2.5 py-1 rounded-xl text-[10px] font-black tracking-wide flex items-center gap-1 shadow-sm">🏆 全站第 1 名</span>`;
    } else if (w.marketRank && w.marketRank <= 10) {
      rankBadge = `<span class="badge-rank-top10 px-2.5 py-1 rounded-xl text-[10px] font-bold flex items-center gap-1">🏅 Top ${w.marketRank}</span>`;
    } else if (w.marketRank) {
      rankBadge = `<span class="px-2 py-0.5 rounded-lg bg-black/60 backdrop-blur-md text-[10px] font-mono text-slate-300 border border-white/10">#${w.marketRank}</span>`;
    }
    
    // Chapters summary
    const chapters = w.chapters || [];
    const nodeCount = chapters.reduce((acc, c) => acc + (c.nodeCount || 0), 0);
    const externalLink = extractLinkFromDesc(w.description);

    // Card Tags: limit to 3, fixed single row with overflow hidden and +N tooltip
    const tags = w.tags || [];
    const MAX_CARD_TAGS = 3;
    const visibleCardTags = tags.slice(0, MAX_CARD_TAGS);
    const hiddenTagsCount = tags.length - MAX_CARD_TAGS;
    const hiddenTagsTooltip = tags.slice(MAX_CARD_TAGS).join('、');
    
    return `
      <div class="work-card bg-white/80 dark:bg-surface-900/80 rounded-3xl border border-slate-200/80 dark:border-slate-800/80 overflow-hidden shadow-sm flex flex-col backdrop-blur-sm relative group">
        <!-- Cover Image -->
        <div class="relative w-full aspect-[16/9] overflow-hidden bg-slate-100 dark:bg-slate-800">
          <img 
            src="${coverUrl}" 
            alt="${w.title}" 
            loading="lazy"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            onerror="this.src='https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&auto=format&fit=crop&q=80'"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent"></div>
          
          <!-- Top Badges -->
          <div class="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="px-2.5 py-1 rounded-xl bg-black/60 backdrop-blur-md text-[11px] font-mono font-bold text-white border border-white/10 shadow-sm">
                v${w.version || '1.0'}
              </span>
              ${rankBadge}
            </div>
            <div class="flex items-center gap-1.5 flex-wrap justify-end">
              ${eventBadge}
              ${aiBadge}
              ${w.releaseNumber ? `<span class="px-2 py-0.5 rounded-full bg-white/20 backdrop-blur-md text-[10px] font-semibold text-white">#${w.releaseNumber} 發布</span>` : ''}
            </div>
          </div>
          
          <!-- Bottom Title overlay on image -->
          <div class="absolute bottom-3 left-3 right-3">
            <h3 class="text-lg font-bold text-white drop-shadow-md tracking-tight leading-snug line-clamp-1">
              ${w.title}
            </h3>
            <p class="text-[11px] text-white/80 font-mono">
              @${author}/${slug}
            </p>
          </div>
        </div>

        <!-- Card Body -->
        <div class="p-5 flex-grow flex flex-col justify-between">
          <div>
            <!-- Tags (Strictly 1 row, uniform 24px height, avoids breaking card heights) -->
            <div class="flex items-center flex-wrap gap-1.5 mb-3 h-6 overflow-hidden">
              ${visibleCardTags.map(t => `<span class="text-[10px] font-medium px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 whitespace-nowrap">${t}</span>`).join('')}
              ${hiddenTagsCount > 0 ? `
                <span 
                  class="text-[10px] font-semibold px-1.5 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-brand-500 dark:hover:text-brand-400 cursor-pointer transition border border-slate-200/50 dark:border-slate-700/50 view-chapters-btn"
                  data-work-id="${w.id}"
                  title="點擊查看全部標籤：${hiddenTagsTooltip}"
                >
                  +${hiddenTagsCount}
                </span>
              ` : ''}
            </div>

            <!-- Description (collapsible) -->
            <div class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed relative mb-4">
              <p class="desc-text line-clamp-3">${w.description || '暫無簡介'}</p>
              ${w.description && w.description.length > 90 ? `
                <button class="expand-btn text-[11px] text-brand-600 dark:text-brand-400 font-semibold mt-1 hover:underline focus:outline-none">展開全文</button>
              ` : ''}
            </div>
          </div>

          <!-- Bottom: Metrics & Actions -->
          <div>
            <!-- Stats Bar -->
            <div class="grid grid-cols-4 gap-1 p-2 rounded-2xl bg-slate-50 dark:bg-surface-950/80 border border-slate-100 dark:border-slate-800/80 text-center mb-4 font-mono">
              <div class="py-1">
                <span class="text-[10px] text-slate-400 block font-sans">瀏覽</span>
                <span class="text-xs font-bold text-slate-800 dark:text-slate-200">${formatNumber(w.views)}</span>
              </div>
              <div class="py-1 border-l border-slate-200/60 dark:border-slate-800">
                <span class="text-[10px] text-slate-400 block font-sans">遊玩</span>
                <span class="text-xs font-bold text-indigo-500">${formatNumber(w.plays)}</span>
              </div>
              <div class="py-1 border-l border-slate-200/60 dark:border-slate-800">
                <span class="text-[10px] text-slate-400 block font-sans">愛心</span>
                <span class="text-xs font-bold text-rose-500">${formatNumber(w.likes)}</span>
              </div>
              <div class="py-1 border-l border-slate-200/60 dark:border-slate-800">
                <span class="text-[10px] text-slate-400 block font-sans">留言</span>
                <span class="text-xs font-bold ${w.unanswered > 0 ? 'text-amber-500' : 'text-slate-800 dark:text-slate-200'}">
                  ${formatNumber(w.comments)}
                  ${w.unanswered > 0 ? `<span class="text-[9px] text-amber-500 block leading-none font-sans">待覆 ${w.unanswered}</span>` : ''}
                </span>
              </div>
            </div>

            <!-- Chapter & Node info -->
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-4 px-1">
              <span>${chapters.length} 個章節 · 共 ${nodeCount} 張卡片</span>
              <button 
                class="view-chapters-btn text-brand-600 dark:text-brand-400 hover:underline font-medium"
                data-work-id="${w.id}"
              >
                查看章節明細 →
              </button>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
              <a 
                href="${playUrl}" 
                target="_blank" 
                class="flex-1 py-2 px-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-sm shadow-brand-500/20"
              >
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>立即遊玩</span>
              </a>

              <a 
                href="${w.marketUrl || `https://larch.ink/market?section=games&game=${w.id}`}" 
                target="_blank" 
                class="py-2 px-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/20 font-medium text-xs transition flex items-center gap-1"
                title="在 Larch 遊戲市集中查看本作品"
              >
                <span>市集專頁</span>
              </a>

              <a 
                href="${workUrl}" 
                target="_blank" 
                class="py-2 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-medium text-xs transition flex items-center gap-1"
                title="Larch 作品原始主頁"
              >
                <span>首頁</span>
              </a>

              ${externalLink ? `
                <a 
                  href="${externalLink}" 
                  target="_blank" 
                  class="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition"
                  title="作品關聯網站"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              ` : ''}
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
  
  // Attach expand / collapse listeners
  worksGridEl.querySelectorAll('.expand-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const p = e.target.previousElementSibling;
      const isClamped = p.classList.contains('line-clamp-3');
      if (isClamped) {
        p.classList.remove('line-clamp-3');
        e.target.textContent = '收起簡介';
      } else {
        p.classList.add('line-clamp-3');
        e.target.textContent = '展開全文';
      }
    });
  });
  
  // Attach chapter detail modal buttons
  worksGridEl.querySelectorAll('.view-chapters-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const workId = btn.dataset.workId;
      const work = allWorks.find(w => w.id === workId);
      if (work) openChapterModal(work);
    });
  });
}

// Chapter Detail Modal
function openChapterModal(work) {
  modalTitleEl.textContent = work.title;
  modalSubtitleEl.textContent = `@${work.authorHandle || 'yaze'}/${work.customSlug || work.id} · 共 ${work.chapters?.length || 0} 章節`;
  modalPlayLinkEl.href = work.playUrl || (work.customSlug ? `https://larch.ink/play/market/${work.authorHandle || 'yaze'}/${work.customSlug}` : `https://larch.ink/play/market/${work.id}`);
  
  const tags = work.tags || [];
  const tagsHtml = tags.length > 0 ? `
    <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-surface-950 border border-slate-100 dark:border-slate-800">
      <div class="text-[11px] font-bold text-slate-400 dark:text-slate-500 mb-2 flex items-center justify-between">
        <span>作品全標籤 (${tags.length})</span>
        ${work.eventId ? `<span class="text-indigo-500 font-normal font-sans">活動：${work.eventId}</span>` : ''}
      </div>
      <div class="flex flex-wrap gap-1.5">
        ${tags.map(t => `<span class="text-xs px-2.5 py-1 rounded-xl bg-white dark:bg-surface-900 border border-slate-200/70 dark:border-slate-700/70 text-slate-700 dark:text-slate-300 font-medium">${t}</span>`).join('')}
      </div>
    </div>
  ` : '';

  const chapters = work.chapters || [];
  const chaptersHtml = chapters.map((c, i) => {
    const cover = c.coverUrl || '';
    return `
      <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-surface-950 border border-slate-100 dark:border-slate-800 flex items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          ${cover ? `<img src="${cover}" class="w-12 h-12 rounded-xl object-cover" />` : `
            <div class="w-12 h-12 rounded-xl bg-slate-200 dark:bg-slate-800 flex items-center justify-center text-xs font-mono font-bold text-slate-500">
              #${i + 1}
            </div>
          `}
          <div>
            <h4 class="text-sm font-bold text-slate-900 dark:text-white">${c.name || `第 ${i + 1} 章`}</h4>
            <p class="text-xs text-slate-400 mt-0.5">${c.description || `${c.nodeCount || 0} 張卡片節點`}</p>
          </div>
        </div>
        <div class="text-right font-mono text-xs text-slate-500">
          <div><span class="text-slate-800 dark:text-slate-200 font-bold">${formatNumber(c.views)}</span> 瀏覽</div>
          <div><span class="text-indigo-500 font-bold">${formatNumber(c.plays)}</span> 遊玩</div>
        </div>
      </div>
    `;
  }).join('');
  
  modalChaptersListEl.innerHTML = tagsHtml + chaptersHtml;
  
  chapterModalEl.classList.remove('hidden');
  setTimeout(() => {
    chapterModalEl.classList.remove('opacity-0');
    chapterModalContentEl.classList.remove('scale-95');
  }, 10);
}

function closeChapterModal() {
  chapterModalEl.classList.add('opacity-0');
  chapterModalContentEl.classList.add('scale-95');
  setTimeout(() => {
    chapterModalEl.classList.add('hidden');
  }, 200);
}

closeModalBtn.addEventListener('click', closeChapterModal);
chapterModalEl.addEventListener('click', (e) => {
  if (e.target === chapterModalEl) closeChapterModal();
});

// Ping Monitor Modal
pingModalBtn.addEventListener('click', () => {
  renderPingModal();
  pingModalEl.classList.remove('hidden');
  setTimeout(() => {
    pingModalEl.classList.remove('opacity-0');
  }, 10);
});

function closePingModal() {
  pingModalEl.classList.add('opacity-0');
  setTimeout(() => {
    pingModalEl.classList.add('hidden');
  }, 200);
}

closePingModalBtn.addEventListener('click', closePingModal);
pingModalEl.addEventListener('click', (e) => {
  if (e.target === pingModalEl) closePingModal();
});

function renderPingModal() {
  if (!pingResults || pingResults.length === 0) {
    pingListContainerEl.innerHTML = `<p class="text-xs text-slate-400 py-8 text-center">暫無巡檢紀錄</p>`;
    return;
  }
  
  pingListContainerEl.innerHTML = `
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead>
          <tr class="border-b border-slate-200 dark:border-slate-800 text-slate-400">
            <th class="pb-2 font-medium">作品名稱</th>
            <th class="pb-2 font-medium">狀態</th>
            <th class="pb-2 font-medium">響應延遲</th>
            <th class="pb-2 font-medium">巡檢網址</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 font-mono">
          ${pingResults.map(p => `
            <tr>
              <td class="py-2.5 font-sans font-semibold text-slate-800 dark:text-slate-200">${p.title}</td>
              <td class="py-2.5">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${
                  p.status === 200 
                    ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' 
                    : 'bg-rose-500/10 text-rose-500'
                }">
                  ${p.status === 200 ? '● 200 OK' : `● ${p.status}`}
                </span>
              </td>
              <td class="py-2.5 text-slate-500">${p.latency_ms || 0} ms</td>
              <td class="py-2.5 text-slate-400 truncate max-w-xs">
                <a href="${p.url}" target="_blank" class="hover:text-brand-500 transition">${p.url}</a>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// Search and Sort listeners
searchInputEl.addEventListener('input', (e) => {
  searchQuery = e.target.value;
  applyFiltersAndRender();
});

sortSelectEl.addEventListener('change', (e) => {
  currentSort = e.target.value;
  applyFiltersAndRender();
});

// ESC key closes modals
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeChapterModal();
    closePingModal();
  }
});

// Initialize
initTheme();
loadData();
