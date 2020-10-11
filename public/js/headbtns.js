var backBtn = document.querySelector('#back-btn')
var logoutBtn = document.querySelector('#logout-btn')

if (backBtn) {
    backBtn.innerHTML = `
    <i class="fas fa-chevron-left"></i>
    `
    backBtn.addEventListener('click', () => {
        history.back()
    })
}

if (logoutBtn){
    logoutBtn.innerHTML = `
    <i class="fas fa-sign-out-alt"></i>
    `
    logoutBtn.addEventListener('click',()=>{
        window.open('/logout','_self')
    })
}