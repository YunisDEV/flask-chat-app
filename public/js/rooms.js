document.querySelectorAll('.room').forEach(i => {
    i.addEventListener('click', (e) => {
        window.open(`/chat/${e.target.getAttribute('room-id')}`,'_self')
    })
})