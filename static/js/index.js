var baseUrl = location.protocol + '//' + document.domain + ':' + location.port

document.getElementById('create').addEventListener('click', () => {
    var height = document.getElementById('height').value
    var width = document.getElementById('width').value
    // window.location.href = `/create-board?height=${height}&width=${width}`
    fetch(`${baseUrl}/create-board?height=${height}&width=${width}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // or response.text(), response.blob(), etc.
        })
        .then(data => {
            console.log('Success:', data);
            window.location.href = `/board/${data.board_id}`
            // fetch(`${baseUrl}/join-board/${data.board_id}`)
            //     .then(response => {
            //         if (response.ok) {
            //             socket.emit('join', {
            //                 board_id: data.board_id
            //             })
            //         }
            //     })
        })
        .catch(error => {
            console.error('There was a problem with the create fetch operation:', error);
        });
})

document.getElementById('join').addEventListener('click', () => {
    var boardId = document.getElementById('id').value;
    if (boardId) {
        window.location.href = `/board/${boardId}`;
    } else {
        console.error('Please enter a valid Board ID');
    }
});
