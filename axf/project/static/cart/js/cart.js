$(document).ready(function(){
    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+"price").innerHTML = data.price  //其他都一样，使用这个来总计价格
                }
            })
        })
    }

//j减
    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+"price").innerHTML = data.price
                    if(data.data == 0) {
                        //window.location.href = "http://127.0.0.1:8001/cart/"     这个是使用刷新界面的办法，特别丑
                        var li = document.getElementById(pid+"li")  //获取显示的li的id
                        li.parentNode.removeChild(li)
                         //元素本身是没有办法删除自己的，找到他的父元素，使用父元素删除他
                    }
                }
            })
        })
    }



    var ischoses = document.getElementsByClassName("ischose")
    for (var j = 0; j < ischoses.length; j++){
        ischose = ischoses[j]
        ischose.addEventListener("click", function(){
            pid = this.getAttribute("goodsid")   //商品的id
            $.post("/changecart/2/", {"productid":pid}, function(data){  //使用post来发起ajax请求
                if (data.status == "success"){
                    //window.location.href = "http://127.0.0.1:8000/cart/"
                    var s = document.getElementById(pid+"a")
                    s.innerHTML = data.data
                }
            })
        },false)
    }



    var ok = document.getElementById("ok")
    ok.addEventListener("click", function(){
        var f = confirm("是否确认下单？")
        if (f){
            $.post("/saveorder/", function(data){  //发起ajx请求
                if (data.status = "success"){
                    window.location.href = "http://127.0.0.1:8000/cart/"
                }
            })
        }
    },false)
})