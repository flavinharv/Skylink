// MUDAR TEMA
const toggle = document.getElementById('btn-tema');
toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const icon = toggle.querySelector('i');
    icon.classList.toggle('bx-moon');
    icon.classList.toggle('bx-sun');
});


// FAZER LOGIN
async function fazerLogin() {
    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value;

    if (!email || !senha) {
        alert("Preencha email e senha.");
        return;
    }

    try {
        const resp = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: email, password: senha })
        });

        const data = await resp.json();

        if (resp.ok && data.sucesso) {
            window.location.href = '/home';
        } else {
            alert(data.mensagem || 'Erro ao logar');
        }
    } catch (err) {
        console.error(err);
        alert('Erro na conexão com o servidor.');
    }
}