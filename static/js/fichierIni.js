const darkToggle = document.getElementById('darkToggle');
const savedMode = localStorage.getItem('dark-mode');

const enableDark = () => {
  document.body.classList.add('dark-mode');
  darkToggle.innerHTML = '<i class="fas fa-sun"></i>';
  localStorage.setItem('dark-mode', 'enabled');
};

const disableDark = () => {
  document.body.classList.remove('dark-mode');
  darkToggle.innerHTML = '<i class="fas fa-moon"></i>';
  localStorage.setItem('dark-mode', 'disabled');
};

if (savedMode === 'enabled') enableDark();
else disableDark();

darkToggle.addEventListener('click', () => {
  document.body.classList.contains('dark-mode') ? disableDark() : enableDark();
});











function searchUser() {
  const input = document.getElementById("searchInput");
  const filter = input.value.toLowerCase();
  const rows = document.querySelectorAll("table tbody tr");

  rows.forEach(row => {
    const filenameCell = row.querySelector("td");
    if (filenameCell) {
      const text = filenameCell.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? "" : "none";
    }
  });
}
