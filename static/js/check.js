function checkform()
{
    var patrn = /^([a-zA-Z0-9_])+@([a-zA-Z0-9_])+\.([a-zA-Z0-9_])+$/;
   // var len =document.theform.comment.value.length; 
    if(document.theform.author.value.length==0)
    {
        alert("请输入昵称!");
        return false;
    }
    if(!patrn.test(document.theform.email.value))
    {
        alert("请输入正确的邮件地址!");
        return false;
    }
    var len = document.theform.comment.value.length;
    if(len==0)
    {
        alert("请输入评论!");
        return false;
    }
    if(len>200)
    {
        alert("请将评论限制在200字以内");
        return false;
    }
    return true;
}


function showchange()
{
    var len = 200-document.theform.comment.value.length;
    var obj = document.getElementById("info");
    if(len>0)
    {
        obj.innerHTML="还可以输入"+len+"字";
        obj.style.color="black";
    }
    else
    {
        obj.innerHTML="已经超出"+(-len)+"字";
        obj.style.color="red";
    }
    return true;
}

function checkusr()
{
    var exp = /^([0-9a-zA-Z_]){6,32}$/;
    if(!exp.test(document.usrinfo.usrname.value))
    {
        alert("请输入6-32位有效的用户名");
        return false;
    }
    var len = document.usrinfo.password.value.length;
    if(len<8||len>255)
    {
        alert("请输入长度在8位以上256位以下的密码");
        return false;
    }
    return true;
}
