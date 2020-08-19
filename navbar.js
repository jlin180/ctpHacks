var xhr_nav = typeof XMLHttpRequest != 'undefined' ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
xhr_nav.open('get', 'navbar.html', true);
xhr_nav.onreadystatechange = function() {
    if (xhr_nav.readyState == 4 && xhr_nav.status == 200) { 
        document.getElementById("navbar-bs").innerHTML = xhr_nav.responseText;
    } 
}
xhr_nav.send();