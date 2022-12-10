if (typeof results !== 'undefined') {
    document.querySelector('img.captured').src = `images/${results.attemptHash}.png`;
    document.body.classList.add('capture');
    window.parent.postMessage(JSON.stringify(results), '*');
    console.log('COMPLETED:', results.completed);
    if (results.completed) {
        document.body.classList.add('completed');
        document.querySelector('.output').innerText = 'Unlocked!';
        document.querySelector('input').disabled = true;
        document.querySelector('button').disabled = true;
    }
}
