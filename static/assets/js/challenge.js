if (localStorage.getItem('group')) {
    window.location.href = `/challenge/${localStorage.getItem('group')}`
}


function validateTeam() {
    let name = document.getElementById('name').value.toUpperCase()
    if (name) {
        document.getElementById('err').style.display = 'none'
        localStorage.setItem('group', name)
        window.location.href = `challenge/${name}`
    } else {
        document.getElementById('err').style.display = 'block'
    }
}

function handle(e) {
    if (e.keyCode === 13) {
        e.preventDefault(); // Ensure it is only this code that rusn
        validateTeam()
    }
}