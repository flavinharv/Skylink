// MUDAR TEMA
const toggle = document.getElementById('btn-tema');
toggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  const icon = toggle.querySelector('i');
  icon.classList.toggle('bx-moon');
  icon.classList.toggle('bx-sun');
});


