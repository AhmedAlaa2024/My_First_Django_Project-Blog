function validate() {
    var x = document.forms["new_post"]["subject"].value;
    var y = document.forms["new_post"]["message"].value;
    if (x == "" && y == "") {
        alert("Subject and message must be filled out.");
        return false;
    } else if (x == "") {
        alert("Subject must be filled out.");
        return false;
    } else if (y == "") {
        alert("Message must be filled out.");
        return false;
    }
}