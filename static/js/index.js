function selectCard(type) {
  const independent = document.getElementById('independent-card');
  const partnered = document.getElementById('partnered-card');
  const expanded = document.getElementById('expanded-content');
  const text = document.getElementById('expanded-text');
  const independentText = document.getElementById('independent-text');
  const partneredText = document.getElementById('partnered-text');

  // Hide the unselected card
  if (type === 'independent') {
    partnered.style.display = 'none';
    independentText.style.display = 'none';
    partneredText.style.display = 'none';
    independent.classList.add('centered-pcard');
    independent.classList.add('animate-from-left');
    } else {
    independent.style.display = 'none';
    partneredText.style.display = 'none';
    independentText.style.display = 'none';
    partnered.classList.add('centered-pcard');
    partnered.classList.add('animate-from-right');
  }
  // Fetch the cheat sheet data
  fetch('/api/cheatsheet')
  .then(res => res.json())
  .then(data => {
    const ul = document.createElement('ul');
    const key = type === 'independent' ? 'solo' : 'partner';
    data.cheatsheet[key].points.forEach(point => {
      const li = document.createElement('li');
      li.textContent = point;
      ul.appendChild(li);
    });
    text.appendChild(ul);
  });
  expanded.classList.remove('d-none');
}

function resetCards() {
  const independent = document.getElementById('independent-card');
  const partnered = document.getElementById('partnered-card');
  const expanded = document.getElementById('expanded-content');
  const independentText = document.getElementById('independent-text');
  const partneredText = document.getElementById('partnered-text');
  const text = document.getElementById('expanded-text');

  // Reset styles and visibility
  independent.style.display = 'block';
  partnered.style.display = 'block';
  
  text.innerHTML = '';
  independent.classList.remove('centered-pcard');
  partnered.classList.remove('centered-pcard');
  independent.classList.remove('animate-from-left');
  partnered.classList.remove('animate-from-right');
  independentText.style.display = 'block';
  partneredText.style.display = 'block';

  expanded.classList.add('d-none');
}
