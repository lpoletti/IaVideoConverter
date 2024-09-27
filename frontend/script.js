// script.js
// Aqui você adicionará o JavaScript para interações e funcionalidades
const searchForm = document.getElementById('searchForm');
const searchResults = document.getElementById('searchResults');
const data = [
  { title: 'Post 1', content: 'Conteúdo do post 1' },
  { title: 'Post 2', content: 'Conteúdo do post 2' },
  // ... outros dados
];

searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();

  const results = data.filter(item => {
    return item.title.toLowerCase().includes(searchTerm) || item.content.toLowerCase().includes(searchTerm);
  });

  searchResults.innerHTML = results.map(item => `<p>${item.title}</p>`).join('');
});