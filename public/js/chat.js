var roomID = location.href.split('/')
var userName = document.querySelector('body').getAttribute('user-name')
roomID = roomID[roomID.length - 1]
document.querySelector('#msg-form').addEventListener('submit', (e) => {
    e.preventDefault()
    socket.emit('send_message', {
        message: e.target.msg.value,
        room: roomID
    })
    e.target.msg.value = ''
})
const autoscroll = () => {
    try {
        $messages = document.querySelector('.messagesBx')
        const $newMessage = $messages.lastElementChild
        const newMessageStyles = getComputedStyle($newMessage)
        const newMessageMargin = parseInt(newMessageStyles.marginBottom)
        const newMessageHeight = $newMessage.offsetHeight + newMessageMargin
        const visibleHeight = $messages.offsetHeight
        const containerHeight = $messages.scrollHeight
        const scrollOffset = $messages.scrollTop + visibleHeight
        $messages.scrollTop = $messages.scrollHeight
    } catch (e) {

    }
    finally { }
}
$(document).ready(() => {
    autoscroll()
    socket.on('message_received', (data) => {
        document.querySelector('.messagesBx').innerHTML += `
            <div class="chatBubbleBx">
                <div class="chatBubble ${data.by==userName?'me':'you'}">
                    <p class="by">${data.by}</p>
                    <p class="body">${data.message}</p>
                    <p class="time">${data.time}</p>
                </div>
            </div>
        `
        autoscroll()
    })
    socket.emit('connected', {
        room: roomID
    })
})
document.addEventListener('click', function (event) {

	// Ignore clicks that weren't on the toggle button
	if (!event.target.hasAttribute('data-toggle-fullscreen')) return;

	// If there's an element in fullscreen, exit
	// Otherwise, enter it
	if (document.fullscreenElement) {
		document.exitFullscreen();
	} else {
		document.documentElement.requestFullscreen();
	}

}, false);