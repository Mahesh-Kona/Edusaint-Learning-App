document.addEventListener('DOMContentLoaded', function () {
  // Toggle sample lesson badge
  const sampleToggle = document.getElementById('sampleLesson');
  const sampleBadge = document.querySelector('.sample-badge');

  if (sampleToggle && sampleBadge) {
    sampleToggle.addEventListener('change', function () {
      sampleBadge.style.display = this.checked ? 'block' : 'none';
    });
  }

  // Add topic → redirect to create_topic.html
  const addTopicBtn = document.querySelector('.btn-primary');
  if (addTopicBtn) {
    addTopicBtn.addEventListener('click', function () {
      // Redirect to Flask admin create topic route
      window.location.href = '/admin/create_topic';
    });
  }

  // Edit topic
  document.querySelectorAll('.action-btn .fa-edit').forEach((btn) => {
    btn.addEventListener('click', function () {
      const topic = this.closest('.topic-card').querySelector('.topic-title').textContent;
      alert(`Editing topic: ${topic}`);
    });
  });

  // Delete topic
  document.querySelectorAll('.action-btn .fa-trash').forEach((btn) => {
    btn.addEventListener('click', function () {
      const topic = this.closest('.topic-card').querySelector('.topic-title').textContent;
      if (confirm(`Are you sure you want to delete "${topic}"?`)) {
        this.closest('.topic-card').remove();
      }
    });
  });
});
