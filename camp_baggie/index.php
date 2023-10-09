<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#SFYL</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">
</head>
<body>

<button class="noass-button">#NOASS</button>


<!-- Floating heads -->
<div id="floating-heads">
    <?php 
    // Scan the 'heads' directory for PNG images
    $dir = "heads/";
    $images = array_merge(glob($dir . "*.png"), glob($dir . "*.jpg"), glob($dir . "*.jpeg"), glob($dir . "*.gif"));
    foreach($images as $image): ?>
        <!-- Add style="position:absolute;" to each img -->
        <img src="<?php echo $image; ?>" class="floating-head" alt="Profile Picture" style="position:absolute;">
    <?php endforeach; ?>
</div>

<script src="scripts.js"></script>

<video autoplay muted loop id="bgVideo">
    <source src="video.mp4" type="video/mp4">
    Your browser does not support HTML5 video.
</video>

<audio id="harlemShakeAudio" src="harlemshake.mp3"></audio>
<div class="flash-overlay"></div>

</body>
</html>
