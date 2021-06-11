window.onscroll = function(e) {
    var otherScrollTop = document.documentElement.scrollTop; //IE & Firefox
    var otherScrollLeft = document.documentElement.scrollLeft; //IE & Firefox
    //alert(otherScrollTop + " - " + otherScrollLeft);

    if (otherScrollTop < 50) {
        document.getElementById("myDIV").style.opacity = "0";
    } else if (otherScrollTop < 100) {
        document.getElementById("myDIV").style.opacity = "0.2";
    } else if (otherScrollTop < 150) {
        document.getElementById("myDIV").style.opacity = "0.4";
    } else if (otherScrollTop < 200) {
        document.getElementById("myDIV").style.opacity = "0.6";
    } else if (otherScrollTop < 250) {
        document.getElementById("myDIV").style.opacity = "0.8";
    } else if (otherScrollTop > 251) {

        document.getElementById("myDIV").style.opacity = "1";
    }
}