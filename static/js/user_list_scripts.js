 document.getElementById('darkToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
  });

// Gestion de la table utilisateurs
let displayedRows = 5;
let currentIndex = 0;

function getFilteredRows() {
  const selectedRole = document.querySelector('input[name="roleFilter"]:checked')?.value || 'tous';
  const searchValue = document.getElementById('searchInput')?.value.toLowerCase() || '';
  const allRows = Array.from(document.querySelectorAll('#userTable tbody tr'));

  return allRows.filter(row => {
    const role = row.getAttribute('data-role');
    const username = row.querySelector('td:first-child').innerText.toLowerCase();
    const matchRole = selectedRole === 'tous' || role === selectedRole;
    const matchSearch = username.includes(searchValue);
    return matchRole && matchSearch;
  });
}

function updateTableDisplay() {
  const allRows = Array.from(document.querySelectorAll('#userTable tbody tr'));
  allRows.forEach(row => row.style.display = 'none');

  const visibleRows = getFilteredRows();
  const totalPages = Math.ceil(visibleRows.length / displayedRows);
  const currentPage = Math.floor(currentIndex / displayedRows) + 1;

  const paginatedRows = visibleRows.slice(currentIndex, currentIndex + displayedRows);
  paginatedRows.forEach(row => row.style.display = '');
  const paginationControls = document.getElementById('paginationControls');
  const pageIndicator = document.getElementById('pageIndicator');

  if (visibleRows.length > displayedRows) {
    paginationControls.style.display = 'flex';
    pageIndicator.textContent = `Page ${currentPage} / ${totalPages}`;
  } else {
    paginationControls.style.display = 'none';
  }
}


function filterByRole() {
  currentIndex = 0;
  updateTableDisplay();
}

function searchUser() {
  currentIndex = 0;
  updateTableDisplay();
}

function sortTable() {
  const table = document.getElementById('userTable');
  const tbody = table.querySelector('tbody');
  const isAscending = table.getAttribute('data-sort') === 'asc';
  const rows = Array.from(tbody.querySelectorAll('tr'));

  rows.sort((a, b) => {
    const nameA = a.querySelector('td:first-child').textContent.trim().toLowerCase();
    const nameB = b.querySelector('td:first-child').textContent.trim().toLowerCase();
    return isAscending ? nameA.localeCompare(nameB) : nameB.localeCompare(nameA);
  });

  rows.forEach(row => tbody.appendChild(row));
  table.setAttribute('data-sort', isAscending ? 'desc' : 'asc');
  updateTableDisplay();
}

function addRow() {
  const totalVisible = getFilteredRows().length;
  if (currentIndex + displayedRows < totalVisible) {
    currentIndex += displayedRows;
    updateTableDisplay();
  }
}

function removeRow() {
  if (currentIndex - displayedRows >= 0) {
    currentIndex -= displayedRows;
    updateTableDisplay();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  updateTableDisplay();
});

// Gestion du Modal "Modifier" et "Ajouter"
document.querySelectorAll('.edit-btn').forEach(button => {
  button.addEventListener('click', function (e) {
    e.preventDefault();
    const modal = document.getElementById('userModal');
    const title = document.getElementById('modalTitle');
    const username = document.getElementById('modalUsername');
    const email = document.getElementById('modalEmail');
    const matricule = document.getElementById('modalMatricule');
    const role = document.getElementById('modalRole');
    const form = document.getElementById('userForm');

    const userId = this.getAttribute('data-id');
    const userNameVal = this.getAttribute('data-username');
    const userEmailVal = this.getAttribute('data-email');
    const userMatriculeVal = this.getAttribute('data-matricule');
    const userRoleVal = this.getAttribute('data-role');

    title.innerText = 'Modifier un utilisateur';
    username.value = userNameVal;
    email.value = userEmailVal;
    matricule.value = userMatriculeVal;
    role.value = userRoleVal;
    form.action = `/admin/edit/${userId}`;
    modal.style.display = 'flex';
  });
});

document.getElementById('addUserBtn').addEventListener('click', function (e) {
  e.preventDefault();
  const modal = document.getElementById('userModal');
  const title = document.getElementById('modalTitle');
  const username = document.getElementById('modalUsername');
  const email = document.getElementById('modalEmail');
  const matricule = document.getElementById('modalMatricule');
  const role = document.getElementById('modalRole');
  const password = document.getElementById('modalPassword');
  const form = document.getElementById('userForm');

  title.innerText = 'Ajouter un utilisateur';
  username.value = '';
  email.value = '';
  matricule.value = '';
  password.value = '';
  role.value = 'admin';
  form.action = '/admin/add';
  modal.style.display = 'flex';
});

document.querySelector('.modal .close').addEventListener('click', () => {
  document.getElementById('userModal').style.display = 'none';
});

window.addEventListener('click', (e) => {
  const modal = document.getElementById('userModal');
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});
