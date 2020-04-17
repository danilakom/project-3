function valid(event){
    var pas = document.getElementById('pass').value
    var cpas = document.getElementById('checkPass').value
    for(i=0;i < cpas.length; i++)
        {

        if(pas[i] != cpas[i] && event.keyCode != 8)
            {
                swal ("Упс!", "Пароли не совпадают!", "error" );
                break;
            }
        }
}