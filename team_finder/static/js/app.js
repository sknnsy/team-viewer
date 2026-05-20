/* ========================================================
   Team Finder — interactive bits
   - Skill autocomplete / add / remove (project page)
   - Share clipboard buttons
   ======================================================== */

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let raw of cookies) {
        const c = raw.trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return null;
}

document.addEventListener('DOMContentLoaded', function () {
    initSkillManager();
    initCopyButtons();
});

/* ===== Skill manager ===== */
function initSkillManager() {
    const block = document.querySelector('[data-skill-manager]');
    if (!block) return;

    const projectId = block.dataset.projectId;
    const list = block.querySelector('[data-skill-list]');
    const input = block.querySelector('[data-skill-input]');
    const results = block.querySelector('[data-autocomplete]');
    const addBtn = block.querySelector('[data-add-btn]');
    const csrf = getCookie('csrftoken');

    if (!input) return;

    let debounceTimer = null;
    let currentResults = [];

    /* Autocomplete fetch */
    input.addEventListener('input', function () {
        const query = input.value.trim();
        clearTimeout(debounceTimer);
        if (!query) {
            results.classList.remove('visible');
            results.innerHTML = '';
            return;
        }
        debounceTimer = setTimeout(() => fetchAutocomplete(query), 200);
    });

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            addSkill(input.value.trim());
        } else if (e.key === 'Escape') {
            results.classList.remove('visible');
        }
    });

    document.addEventListener('click', function (e) {
        if (!block.contains(e.target)) {
            results.classList.remove('visible');
        }
    });

    if (addBtn) {
        addBtn.addEventListener('click', function (e) {
            e.preventDefault();
            addSkill(input.value.trim());
        });
    }

    /* Remove skill (event delegation) */
    list.addEventListener('click', function (e) {
        const btn = e.target.closest('[data-remove-skill]');
        if (!btn) return;
        e.preventDefault();
        const skillId = btn.dataset.removeSkill;
        const tag = btn.closest('.skill-tag');
        removeSkill(skillId, tag);
    });

    function fetchAutocomplete(query) {
        const url = block.dataset.autocompleteUrl + '?q=' + encodeURIComponent(query);
        fetch(url, { credentials: 'same-origin' })
            .then(r => r.json())
            .then(data => {
                currentResults = data.results || [];
                renderAutocomplete(query);
            })
            .catch(() => { results.classList.remove('visible'); });
    }

    function renderAutocomplete(query) {
        results.innerHTML = '';
        const existing = new Set(
            Array.from(list.querySelectorAll('.skill-tag'))
                .map(t => (t.dataset.skillName || '').toLowerCase())
        );
        const exactExists = currentResults.some(
            r => r.name.toLowerCase() === query.toLowerCase()
        );

        currentResults.forEach(item => {
            if (existing.has(item.name.toLowerCase())) return;
            const el = document.createElement('div');
            el.className = 'autocomplete-item';
            el.textContent = item.name;
            el.addEventListener('mousedown', function (e) {
                e.preventDefault();
                addSkill(item.name);
            });
            results.appendChild(el);
        });

        if (query.length >= 1 && !exactExists && !existing.has(query.toLowerCase())) {
            const createEl = document.createElement('div');
            createEl.className = 'autocomplete-item autocomplete-item-create';
            createEl.textContent = '＋ Создать «' + query + '»';
            createEl.addEventListener('mousedown', function (e) {
                e.preventDefault();
                addSkill(query);
            });
            results.appendChild(createEl);
        }

        if (results.children.length > 0) {
            results.classList.add('visible');
        } else {
            results.classList.remove('visible');
        }
    }

    function addSkill(name) {
        if (!name) return;
        const existing = Array.from(list.querySelectorAll('.skill-tag'))
            .map(t => (t.dataset.skillName || '').toLowerCase());
        if (existing.includes(name.toLowerCase())) {
            input.value = '';
            results.classList.remove('visible');
            return;
        }

        const url = block.dataset.addUrl;
        const formData = new FormData();
        formData.append('name', name);

        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf },
            body: formData,
            credentials: 'same-origin',
        })
            .then(r => {
                if (!r.ok) throw new Error('add failed');
                return r.json();
            })
            .then(data => {
                appendSkillTag(data);
                input.value = '';
                results.classList.remove('visible');
                results.innerHTML = '';
                input.focus();
            })
            .catch(() => alert('Не удалось добавить навык.'));
    }

    function appendSkillTag(data) {
        const empty = list.querySelector('.skill-empty');
        if (empty) empty.remove();
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.dataset.skillId = data.id;
        tag.dataset.skillName = data.name;
        tag.innerHTML =
            data.name +
            '<button type="button" class="skill-tag-remove" data-remove-skill="' +
            data.id +
            '" aria-label="Удалить">×</button>';
        list.appendChild(tag);
    }

    function removeSkill(skillId, tagEl) {
        const url = block.dataset.removeUrlTemplate.replace('__ID__', skillId);
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf },
            credentials: 'same-origin',
        })
            .then(r => {
                if (!r.ok) throw new Error('remove failed');
                return r.json();
            })
            .then(() => {
                if (tagEl) tagEl.remove();
                if (list.querySelectorAll('.skill-tag').length === 0) {
                    const empty = document.createElement('span');
                    empty.className = 'skill-empty';
                    empty.style.color = 'var(--muted)';
                    empty.style.fontSize = '0.9rem';
                    empty.textContent = 'Навыков пока нет.';
                    list.appendChild(empty);
                }
            })
            .catch(() => alert('Не удалось удалить навык.'));
    }
}

/* ===== Copy-to-clipboard ===== */
function initCopyButtons() {
    document.querySelectorAll('[data-copy-target]').forEach(btn => {
        btn.addEventListener('click', function () {
            const targetSelector = btn.dataset.copyTarget;
            const target = document.querySelector(targetSelector);
            const text = target ? (target.value || target.textContent) : btn.dataset.copyText;
            if (!text) return;

            const fallback = () => {
                if (target && target.select) {
                    target.select();
                    try { document.execCommand('copy'); } catch (e) {}
                }
            };

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(showCopied).catch(fallback);
            } else {
                fallback();
                showCopied();
            }

            function showCopied() {
                const original = btn.textContent;
                btn.textContent = 'Скопировано ✓';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = original;
                    btn.classList.remove('copied');
                }, 1600);
            }
        });
    });
}
