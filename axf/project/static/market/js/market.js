$(document).ready(function(){
//    找到全部类型，综合排序的那个显示的控件
    var alltypebtn = document.getElementById("alltypebtn")
    var showsortbtn = document.getElementById("showsortbtn")
//找到类型的，和排序的控件
    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")
//找到之后默认他们是隐藏的    所以给他们的display是none
    typediv.style.display = "none"
    sortdiv.style.display = "none"

    alltypebtn.addEventListener("click",function(){
        typediv.style.display = "block"
        sortdiv.style.display = "none"

    },false)

    showsortbtn.addEventListener("click",function(){
        typediv.style.display = "none"
        sortdiv.style.display = "block"

    },false)


//点击完成后，点击其他的地方就让这个隐藏，消失
    typediv.addEventListener("click",function(){
        typediv.style.display = "none"
//        sortdiv.style.display = "block"

    },false)


//点击完成后，点击其他的地方就让这个隐藏，消失
    sortdiv.addEventListener("click",function(){
//        typediv.style.display = "none"
        sortdiv.style.display = "none"

    },false)




//    修改购物车

    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")


    for (var i = 0; i< addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")  //通过ga属性  拿到商品的ID
            $.post("/changecart/0/", {"productid":pid}, function(data){
                if (data.status == "success"){
                //添加成功，把中间的span的innerHTML变成当前的数量
                  document.getElementById(pid).innerHTML = data.data
                }else{
                    if (data.data == -1){//view视图中返回判断没有的登录就返回登录界面
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }

            }

        })

    })

    }

//减少购物车
    for (var i = 0; i< subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")  //通过ga属性  拿到商品的ID
            $.post("/changecart/1/", {"productid":pid}, function(data){
                if (data.status == "success"){
                //添加成功，把中间的span的innerHTML变成当前的数量
                  document.getElementById(pid).innerHTML = data.data
                }else{
                    if (data.data == -1){//view视图中返回判断没有的登录就返回登录界面
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }

            }

        })

    })

    }





})