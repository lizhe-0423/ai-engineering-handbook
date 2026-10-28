/* Offline interactions only. No fetch, analytics, external APIs or persistence. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const cases = $$('[data-case]');
  function selectCase(button) {
    const selected = button.dataset.case;
    cases.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    $$('.case-panel').forEach(p => { p.hidden = p.id !== `case-${selected}`; });
    const panel = $(`#case-${selected}`);
    const announce = $('#case-announcement');
    if (announce) announce.textContent = `${button.textContent.trim()}。${$('.case-caption p', panel).textContent}`;
  }
  cases.forEach((button, index) => {
    button.addEventListener('click', () => selectCase(button));
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? cases.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + cases.length) % cases.length;
      cases[next].focus(); selectCase(cases[next]);
    });
  });

  const quiz = $('.quiz');
  if (quiz) {
    const buttons = $$('[data-answer]', quiz);
    buttons.forEach(button => button.addEventListener('click', () => {
      buttons.forEach(b => { b.setAttribute('aria-pressed', String(b === button)); b.classList.remove('correct', 'incorrect'); });
      const correct = button.dataset.answer === quiz.dataset.correct;
      button.classList.add(correct ? 'correct' : 'incorrect');
      const feedback = $('.quiz-feedback', quiz);
      feedback.hidden = false;
      feedback.textContent = (correct ? '对。' : '再想一下。') + quiz.dataset.reason;
    }));
  }

  const dialog = $('#zoom');
  if (dialog) {
    let opener;
    $$('[data-zoom]').forEach(button => button.addEventListener('click', () => {
      opener = button;
      const image = $('img', dialog);
      image.src = button.dataset.zoom;
      image.alt = button.dataset.alt;
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else { dialog.setAttribute('open', ''); dialog.scrollIntoView(); }
      $('[data-close-zoom]', dialog).focus();
    }));
    $('[data-close-zoom]', dialog).addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => { if (opener) opener.focus(); });
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
  }

  const search = $('#chapter-search');
  if (search) {
    let filter = 'all';
    const filters = $$('[data-filter]');
    function applyFilters() {
      const query = search.value.trim().normalize('NFKC').toLocaleLowerCase();
      let count = 0;
      $$('.catalog-group').forEach(group => {
        let visible = 0;
        $$('.chapter-row', group).forEach(row => {
          const matches = (filter === 'all' || group.dataset.group === filter) && row.dataset.search.normalize('NFKC').toLocaleLowerCase().includes(query);
          row.hidden = !matches; if (matches) visible++;
        });
        group.hidden = visible === 0; count += visible;
      });
      $('#search-count').textContent = `${count} 篇图解` + (query || filter !== 'all' ? '符合当前条件' : ' · 每篇都有可切换的情况演示');
      $('#empty-search').hidden = count > 0;
    }
    search.addEventListener('input', applyFilters);
    search.addEventListener('search', applyFilters);
    filters.forEach(button => button.addEventListener('click', () => {
      filter = button.dataset.filter;
      filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      applyFilters();
    }));
  }

  const progress = $('.reading-progress');
  if (progress) {
    let queued = false;
    function draw() {
      const range = document.documentElement.scrollHeight - innerHeight;
      progress.style.width = `${range > 0 ? Math.min(100, Math.max(0, scrollY / range * 100)) : 100}%`;
      queued = false;
    }
    addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(draw); } }, { passive: true });
    addEventListener('resize', draw); draw();
  }
})();
