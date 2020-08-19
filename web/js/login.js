const signInDiv = document.getElementById("sign-in-div");
const signUpDiv = document.getElementById("sign-up-div");
const signInBtn = document.getElementById("sign-in-btn");
const signUpBtn = document.getElementById("sign-up-btn");

signInBtn.onclick = function() {
    signInBtn.style.textDecoration = 'underline';
    signUpBtn.style.textDecoration = 'none';

    signInDiv.style.display = "block";
    signUpDiv.style.display = "none";
}

signUpBtn.onclick = function() {
    signInBtn.style.textDecoration = 'none';
    signUpBtn.style.textDecoration = 'underline';
    
    signInDiv.style.display = "none";
    signUpDiv.style.display = "block";
}