$(document).ready(function(){
//获取相应 的id
    var accunt = document.getElementById("accunt")
//如果发生错误就显示错误的ID
    var accunterr = document.getElementById("accunterr")
    var checkerr = document.getElementById("checkerr")

    var pass = document.getElementById("pass")
    var passerr = document.getElementById("passerr")

    var passwd = document.getElementById("passwd")
    var passwderr = document.getElementById("passwderr")

//聚焦和离焦的事件
    accunt.addEventListener("focus", function(){
        accunterr.style.display = "none"
        checkerr.style.display = "none"
    },false)
    accunt.addEventListener("blur", function(){
//    利用instr来获取当前表单的值，这样就会获取用户名
        instr = this.value
        if (instr.length < 6 || instr.length > 12){
            accunterr.style.display = "block"
            return
        }

//         q请求这个网址    将用户名传入  传入到验证的视图里面
        $.post("/checkuserid/", {"userid":instr}, function(data){
            if (data.status == "error"){
                checkerr.style.display = "block"
            }
        })
    },false)





//通过 的的验证，上面是账户的验证

//聚焦和离焦的事件
    pass.addEventListener("focus", function(){
        passerr.style.display = "none"
    },false)
    pass.addEventListener("blur", function(){
//    利用instr来获取当前表单的值，这样就会获取用户名
        instr = this.value
        if (instr.length < 6 || instr.length > 16){
            passerr.style.display = "block"
            return
        }

//         q请求这个网址    将用户名传入  传入到验证的视图里面
        $.post("/checkuserid/", {"userid":instr}, function(data){
            if (data.status == "error"){
                passerr.style.display = "block"
            }
        })
    },false)




//密码的验证，上面是账户的验证

//聚焦和离焦的事件
    passwd.addEventListener("focus", function(){
        passerr.style.display = "none"
    },false)
    passwd.addEventListener("blur", function(){
//    利用instr来获取当前表单的值，这样就会获取用户名
        instr = this.value
        if (instr.length < 6 || instr.length > 16){
            passwderr.style.display = "block"
            return
        }
    },false)
})



