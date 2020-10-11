document.getElementById('room-form').addEventListener('submit', (e) => {
    e.preventDefault()
    var roomname = e.target.roomname.value
    var password = e.target.password.value
    fetch('/create', {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            roomname,
            password
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.open(`/chat/${data.roomId}`, '_self')
            } else {
                window.alert(data.message)
            }
        })
})