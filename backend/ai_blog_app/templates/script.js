// Função para colapsar a barra lateral no clique do botão
document.querySelector('.sidebar-toggle').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapse');
});

// Simulação de login/logout funcional com Django
document.getElementById('loginForm').addEventListener('submit', function(event) {
    {% comment %} event.preventDefault(); {% endcomment %}
    // Aqui você pode adicionar a chamada Ajax para Django
    alert('Login realizado com sucesso!');
});
