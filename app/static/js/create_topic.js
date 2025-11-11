document.addEventListener('DOMContentLoaded', function () {
    // ========== Add Learning Objective ==========
    const addObjectiveBtn = document.querySelector('.add-objective');
    const objectivesList = document.querySelector('.objectives-list');

    addObjectiveBtn.addEventListener('click', function () {
        const objectiveCount = objectivesList.querySelectorAll('.objective-item').length;
        const newObjective = document.createElement('div');
        newObjective.className = 'objective-item';
        newObjective.innerHTML = `
            <div class="objective-number">${objectiveCount + 1}</div>
            <input type="text" class="objective-input" placeholder="Add learning objective...">
        `;
        objectivesList.insertBefore(newObjective, addObjectiveBtn);
    });

    // ========== Add New Card ==========
    const addCardBtn = document.querySelector('.add-card');
    const cardsGrid = document.getElementById('cardsGrid');

    addCardBtn.addEventListener('click', function () {
        // Open the React-based topic editor in a new tab.
        // This route serves files from the repository's topic-editor/topic-editor folder.
        // If you run a Vite/React dev server, you may prefer to open http://localhost:5173 instead.
        try {
            // Prefer the local Vite dev server if a developer is running it.
            // Try opening http://localhost:5173 first (common Vite default). If that
            // returns null (popup blocked) or fails, fall back to the Flask route.
            const devUrl = 'http://localhost:5173';
            const adminUrl = '/admin/topic-editor/';
            let win = null;
            try {
                // open in the same tab/window as requested
                win = window.open(devUrl, '_self');
            } catch (e) {
                console.debug('Opening dev server threw, will fallback to admin route', e);
                win = null;
            }

            // If popup blocked (win is null) or window couldn't be opened, try admin route
            if (!win) {
                try {
                    // fallback: open the Flask-served editor in the same tab
                    win = window.open(adminUrl, '_self');
                } catch (err) {
                    console.error('Failed to open topic editor (admin route) as fallback:', err);
                    win = null;
                }
            }

            if (!win) {
                throw new Error('Popup blocked or failed to open editor');
            }
        } catch (err) {
            console.error('Failed to open topic editor:', err);
            // fallback: create an inline card if popup blocked
            const newCard = document.createElement('div');
            newCard.className = 'card-item';
            newCard.innerHTML = `
                <div class="card-header">
                    <div class="card-type">
                        <i class="fas fa-align-left"></i>
                        <span>New Card</span>
                    </div>
                    <div class="card-actions">
                        <button class="card-action"><i class="fas fa-edit"></i></button>
                        <button class="card-action"><i class="fas fa-trash"></i></button>
                    </div>
                </div>
                <div class="card-content">
                    <div class="card-preview">New card content goes here...</div>
                </div>
                <div class="card-meta">
                    <div>
                        <span class="card-difficulty difficulty-easy">Easy</span>
                        <span>• 30 sec</span>
                    </div>
                    <span>LO1</span>
                </div>
            `;
            cardsGrid.appendChild(newCard);
            attachCardEventListeners(newCard);
        }
    });

    // ========== Card Type Selection ==========
    const cardTypeOptions = document.querySelectorAll('.card-type-option');
    cardTypeOptions.forEach(option => {
        option.addEventListener('click', function () {
            cardTypeOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // ========== Edit and Delete Card Actions ==========
    function attachCardEventListeners(card) {
        const editBtn = card.querySelector('.fa-edit');
        const deleteBtn = card.querySelector('.fa-trash');

        editBtn.addEventListener('click', function () {
            const cardType = card.querySelector('.card-type span').textContent;
            alert(`Editing ${cardType} card`);
        });

        deleteBtn.addEventListener('click', function () {
            const cardType = card.querySelector('.card-type span').textContent;
            if (confirm(`Are you sure you want to delete this "${cardType}" card?`)) {
                card.remove();
            }
        });
    }

    // Attach to existing cards
    document.querySelectorAll('.card-item').forEach(card => {
        attachCardEventListeners(card);
    });

    // ========== Save Topic ==========
    const saveBtn = document.querySelector('.btn-primary');
    saveBtn.addEventListener('click', function (ev) {
        // Prevent the default form submit since we handle saving via AJAX below.
        if (ev && ev.preventDefault) ev.preventDefault();
        // disable button to avoid double-submits
        saveBtn.disabled = true;
        const title = document.getElementById('topicTitle').value.trim();
        if (!title) {
            alert('Please fill in the topic title.');
            return;
        }

        // determine lesson id: prefer explicit selector, fall back to URL param
        let lessonId = null;
        const lessonSelect = document.getElementById('lessonSelect');
        if (lessonSelect) lessonId = lessonSelect.value;
        if (!lessonId) {
            const params = new URLSearchParams(window.location.search);
            lessonId = params.get('lesson_id');
        }
        if (!lessonId) { alert('Please select a lesson to attach this topic to.'); return; }

        // collect objectives
        const objectives = Array.from(document.querySelectorAll('.objective-input')).map(el => el.value.trim()).filter(Boolean);

        // collect cards
        const cards = [];
        document.querySelectorAll('.card-item').forEach(card => {
            const type = card.querySelector('.card-type span') ? card.querySelector('.card-type span').textContent.trim() : '';
            const preview = card.querySelector('.card-preview') ? card.querySelector('.card-preview').textContent.trim() : '';
            cards.push({ type, preview });
        });

        const payload = { title, description: document.getElementById('topicDescription') ? document.getElementById('topicDescription').value.trim() : '', objectives, cards, lesson_id: lessonId };

        fetch('/admin/create_topic', { method: 'POST', body: JSON.stringify(payload), credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.json())
            .then(json => {
                if (json && json.success) {
                    alert('Topic created. Redirecting to lesson page...');
                    window.location.href = `/admin/lesson?lesson_id=${lessonId}`;
                } else {
                    alert('Failed to create topic');
                    console.error(json);
                    saveBtn.disabled = false;
                }
            }).catch(err => { console.error(err); alert('Failed to create topic'); saveBtn.disabled = false; });
    });

    // ========== Cancel Button ==========
    const cancelBtn = document.querySelector('.btn-outline');
    cancelBtn.addEventListener('click', function () {
        if (confirm('Are you sure you want to cancel creating this topic?')) {
            // redirect to the admin lesson listing/page
            window.location.href = '/admin/lesson';
        }
    });
});
