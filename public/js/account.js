document.getElementById('account-form').addEventListener('submit', (e) => {
    e.preventDefault()
    var username = e.target.username.value
    var password = e.target.password.value
    fetch('/user', {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.open(`/rooms`, '_self')
            } else {
                window.alert(data.message)
            }
        })
})