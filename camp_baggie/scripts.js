console.log("Script loaded!");

let isRaining = false;

document.querySelector('.noass-button').addEventListener('click', function() {
    let button = document.querySelector('.noass-button');
    let audio = document.getElementById('harlemShakeAudio');
    let heads = document.querySelectorAll('.floating-head');
    let floatingHeadsContainer = document.getElementById('floating-heads');
    
    if (!isRaining) {
        button.classList.add('clicked');
        audio.play();
        floatingHeadsContainer.style.display = 'block';
        
heads.forEach((head, index) => {
    let animationDuration = (Math.random() * 5 + 5) + 's';
    let headSize = (Math.random() * 10 + 5) + 'vw';

    head.style.top = '-' + (Math.random() * 100 + 50) + 'px';
    head.style.animation = `falling ${animationDuration} linear infinite`;
    
    // Adjust the left positioning to allow heads to start a bit outside and go a bit outside
    head.style.left = (Math.random() * 120 - 10) + 'vw'; // Range from -10vw to 110vw
    
    head.style.maxWidth = headSize;
});



        
        isRaining = true;
    } else {
        button.classList.remove('clicked');
        audio.pause();
        audio.currentTime = 0;
        floatingHeadsContainer.style.display = 'none';
        
        heads.forEach(head => {
            head.style.animation = '';
        });

        isRaining = false;
    }
});
