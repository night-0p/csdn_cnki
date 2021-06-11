var hobbies = document.getElementsByName("item");
checkAll.onclick = function() {
    if (checkAll.checked) { //全选
        for (var i = 0; i < hobbies.length; i++) {
            hobbies[i].checked = true;
        }
    } else { //取消全选
        for (var i = 0; i < hobbies.length; i++) {
            hobbies[i].checked = false;
        }
    }
}