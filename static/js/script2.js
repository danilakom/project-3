function passcorr() {
    var pass = document.getElementById("pass").value;
    var p = /^[a-zA-Z0-9]+$/;
    if (p.test(pass)) {
        err = "";
    }
    else {
        err = "<font color=\'red\'> Введены недопустимые символы! Разрешены только латинские буквы и цифры!</font>";
        document.getElementById("err").innerHTML=err;
        exit;
    }

    if (pass.length >= 8) {
            err = "";
    }
    else {
        err = "<font color=\'red\'>Пароль неверной длины. Пароль должен быть не менее 8 символов!</font>";
        document.getElementById("err").innerHTML=err;
        exit;
    }

    var lowerCaseLetters = /[a-z]/g;
    if (pass.match(lowerCaseLetters)) {
        err = "";
    }
    else {
        err = "<font color=\'red\'>Пароль должен содержать хотя бы одну строчную букву!</font>";
        document.getElementById("err").innerHTML=err;
        exit;
    }

    var upperCaseLetters = /[A-Z]/g;
    if (pass.match(upperCaseLetters)) {
        err = "";
    }
    else {
        err = "<font color=\'red\'>Пароль должен содержать хотя бы одну заглавную букву!</font>";
        document.getElementById("err").innerHTML=err;
        exit;
    }

    var numbers = /[0-9]/g;
    if (pass.match(numbers)) {
        err = "<font color=\'green\'>Успешно!</font>";
    }
    else {
        err = "<font color=\'red\'>Пароль должен содеражть хотя бы одну цифру!</font>";
        document.getElementById("err").innerHTML=err;
        exit;
    }
    document.getElementById("err").innerHTML=err;
}