window.onload = () => {
    var values = document.getElementsByClassName('hours');
    var number = parseInt(values[0].textContent);
    var redNum = 0;
    var greenNum = 0;
    var blueNum = 0;
    if(number >= 85){
      greenNum = 255;
    }else if(number < 42.5){
        greenNum = 0;
      redNum = 255;
      greenNum += 6 * number;
    }else{
        redNum = 255;
      greenNum = 255;
      redNum -= 6 * (number - 42.5);
    }
    for (var i = 0; i < values.length; i++) {
      values[i].style.backgroundColor = "rgb(" + redNum + ", " + greenNum + ", 0)";
    }
}