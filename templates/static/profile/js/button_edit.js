const btnEdit = document.querySelector('[data-edit-profile-btn]')
const formDiv = document.querySelector('#profile_edit_form_container')

btnEdit.addEventListener('click', ()=> {
    formDiv.classList.toggle('d-none')
    if (formDiv.classList.contains('d-none')) {
        btnEdit.textContent = 'Edit Profile'
    } else {
        btnEdit.textContent = 'Close Edit'
    }
})