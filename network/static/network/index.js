function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.like').forEach(button => {
        button.onclick = function() {
            const post_id = this.dataset.id
            const heart = this.className
            
            fetch('/like', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({'post_id': post_id, 'heart': heart})
            })
            .then(response => {
                return response.json()
            })
            .then(data => {
                const likes = data['likes']
                this.classList.toggle('red');
                // Update the value of likes in html
                document.querySelector(`#post${post_id}`).innerHTML = likes
            })
        }
    })

    document.querySelectorAll('.follow-btn').forEach(button => {
        button.onclick = () => {
            var btn_value = button.dataset.follow;
            var user_id = button.dataset.user_id;
            fetch('/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({'btn_value': btn_value, 'user_id': user_id})
            })
            .then(response => {
                return response.json()
            })
            .then(data => {
                alert(data)
                location.reload()
            })
        }
    })
})