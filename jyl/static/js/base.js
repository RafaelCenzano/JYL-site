function countWords(text) {
    return text.length || 0;
}

function jsRequired(ta, required){
    ta.addEventListener('input', () => {
        if (countWords(ta.value) > 0){
            required.style.display = 'none';
        }else {
            required.style.display = 'inline-block';
        }
    });
}