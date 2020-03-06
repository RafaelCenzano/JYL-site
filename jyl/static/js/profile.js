var values = document.getElementsByClassName('hours');
var number = parseInt(values[0].value);
var redNum = 0;
var greenNum = 0;
if (number >= 85) {
  greenNum = 255;
} else if (number > (42.5)) {
  greenNum = 255;
  redNum = 255;
  var multiplyer = number - 42.5;
  redNum -= 6 * multiplyer;
} else {
  greenNum = 0;
  redNum = 255;
  var multiplyer = number - 42.5;
  redNum += 6 * multiplyer;
}
for (var i = 0; i < values.length; i++) {
  values[i].style.backgroundColor = "rgb(" + redNum + ", " + greenNum + ", 60)";
}
