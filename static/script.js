document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendationForm');
    const mentorList = document.getElementById('mentorList');
    const results = document.getElementById('results');
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
  
      const data = {
        preferred_subject: form.preferred_subject.value.trim(),
        target_college: form.target_college.value.trim(),
        prep_level: parseInt(form.prep_level.value),
        learning_style: form.learning_style.value.trim()
      };
  
      const res = await fetch('/get_recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
  
      const response = await res.json();
      mentorList.innerHTML = '';
      results.style.display = 'block';
  
      if (response.mentors.length === 0) {
        mentorList.innerHTML = '<div class="alert alert-warning">No suitable mentors found.</div>';
        return;
      }
  
      response.mentors.forEach(mentor => {
        const item = document.createElement('div');
        item.className = 'list-group-item p-3';
  
        item.innerHTML = `
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center">
            <div class="mb-2 mb-md-0">
              <h5>${mentor.name}</h5>
              <p class="mb-1">⭐ Rating: ${mentor.rating.toFixed(2)}</p>
              <p class="mb-0">🎯 Match Score: ${mentor.match_score}</p>
            </div>
            <div>
              <label for="rate-${mentor.name}" class="form-label mb-1">Rate this mentor</label>
              <div class="d-flex align-items-center">
                <input type="number" class="form-control form-control-sm me-2" id="rate-${mentor.name}" min="1" max="5" placeholder="1-5" />
                <button class="btn btn-success btn-sm" onclick="submitRating('${mentor.name}')">Submit</button>
              </div>
            </div>
          </div>
        `;
        mentorList.appendChild(item);
      });
    });
  });
  
  async function submitRating(mentorName) {
    const ratingInput = document.getElementById(`rate-${mentorName}`);
    const rating = parseFloat(ratingInput.value);
  
    if (!rating || rating < 1 || rating > 5) {
      alert('Please enter a valid rating between 1 and 5.');
      return;
    }
  
    await fetch('/rate_mentor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mentor_name: mentorName, rating })
    });
  
    alert('Thank you! Your rating has been submitted.');
    ratingInput.value = '';
  }
  