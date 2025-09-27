document.addEventListener('DOMContentLoaded', function(){
    /* Capture mouse position
    let mouseX = 0;
    let mouseY = 0;
    document.addEventListener('mousemove', function(e){
        mouseX = e.pageX;
        mouseY = e.pageY;
    });
    */

    /* Window width and height
    let windowX = window.innerWidth;
    let windowY = window.innerHeight;
    */

    /* Document width and height
    let documentX = document.documentElement.scrollWidth;
    let documentY = document.documentElement.scrollHeight;
    */

    /* The vertical scroll position is the same as the number of pixels
        that are hidden from view above the scrollable area.
    let scrollPos = window.pageYOffset || document.documentElement.scrollTop;
    */

    /* Sample JSON Ajax call using modern fetch API
    fetch('ajax.php?action=doSomething')
        .then(response => response.json())
        .then(json => {
            document.getElementById('container').innerHTML = json.output;
        })
        .catch(error => console.error('Error:', error));
    */

    // Draggable dialog window using modern modal approach
    // const modal = new bootstrap.Modal(document.querySelector('.fade-in'));
    // modal.show();
});
