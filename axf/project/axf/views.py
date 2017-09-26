from django.shortcuts import render,redirect
import time
import random,os
from django.conf import settings
from .models import Wheel,Nav,Mustbuy,Shop,MainShow,FoodTypes,Goods,User,Cart,Order
# Create your views here.
def home(request):
    wheelsList = Wheel.objects.all()
    navList =Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()

    shopList = Shop.objects.all()   #将便利店引入，一共分为四个部分，将数据拿出去
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    mainList = MainShow.objects.all()  #将最后的静态文件引入

    return render(request, 'axf/home.html',
                  {"title":"主页",
                    "wheelsList":wheelsList,
                   "navList":navList,
                   "mustbuyList":mustbuyList,
                   "shop1":shop1,"shop2":shop2,"shop3":shop3,"shop4":shop4,
                   "mainList": mainList})

#从模型中获取数据，当点击的时候就会获取对应的id
def market(request, categoryid, cid, sortid):  #一开始进不去是因为路径的问题，不能在进入原始的market路径了
    leftSlider = FoodTypes.objects.all()   #左侧的导航栏   加载全部的数据

    if cid =='0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childcid = cid)


    #排序
    if sortid=='1':
        productList = productList.order_by("productnum")  #是按照销量进行排行的
    elif sortid =='2':
        productList = productList.order_by("price")  # 是按照价格进行排行的因为价格是字符串，所以有bug
    elif sortid =='3':
        productList = productList.order_by("-price")  # 是按照价格行排行的



    # #上面的分类的字段
    group = leftSlider.get(typeid=categoryid)    #点击获取相应的id，对这个ID进行处理，得到想要的分类数据
    childList = []
    # chilnames拿出来的是一整个字段，需要切割
    # 一整个字段是：# 全部分类:0#进口水果:103534#国产水果:103533
    chilnames = group.childtypenames
    arr1 = chilnames.split("#")
    for str in arr1:
        # 全部分类0
        arr2 = str.split(":")
        obj = {"childName": arr2[0], "childId": arr2[1]}
        print(arr2[0], arr2[1])
        childList.append(obj)  # 将切割好的数据存入到childList的列表中

    #在进入超市的要进入购物车中去获取全部的 数据，将购物车中购买商品的数量显示出来
    cartlist =[]
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken = token)
        cartlist = Cart.objects.filter(userAccount = user.userAccount)

#判定商品列表和购物车中的ID是不是相等，要是相等就说明购物车中有这个ID，取出那个数量
    for p in productList:
        for c in cartlist:
            if c.productid ==p.productid:
                p.num = c.productnum   #要是购物车中有这个商品就取出他的数量
                continue

    return render(request,'axf/market.html',{"闪送":"闪送超市",
                                             "leftSlider":leftSlider,
                                             "productList":productList,
                                             "childList":childList,
                                             "categoryid":categoryid,"cid":cid
                                             })
    #categoryid是组的ID ， cid是子组的ID
                # "childList":childList}将上面切割好的数据进行返回
                #"categoryid":categoryid  返回一个组的ID 供后面的跳转（全部分类）调用


#将当前购物车的所有信息拿出来，在所有的
def cart(request):
    cartslist = []
    token = request.session.get("token")  #通过token来判断是不是登录了
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount = user.userAccount)  #登录了就拿数据

#将选中的商品添加到购物车里面
    return render(request, 'axf/cart.html', {"title":"购物车","cartslist":cartslist})

#修改购物车
def changecart(request, flag):
    # 判断用户是否登录  查看用户是否有session  没有就是没有登录
    token = request.session.get("token")
    if token == None:
        # 没登录   直接返回一个网页（重定向）是没用的
        #要返回一个json数据，让js接收，并且返回界面
        return JsonResponse({"data": -1, "status": "error"})

    productid = request.POST.get("productid")  #获取商品的id
    product = Goods.objects.get(productid = productid)  #通过商品的ID拿出商品
    user = User.objects.get(userToken = token)  #根据token值获取用户的id

    if flag == '0':
        if product.storenums == 0:   #判断是不是库存已经没有了，如果没有库存，直接不进行下一步
            return JsonResponse({"data": -2, "status": "error"})
        # 将用户的所有的购物车数据全部拿出来
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单   增加订单的拿出订单的所有的信息，名字拿出长名字，通过上面定义的商品来拿
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, False)
            c.save()  # 保存
            pass
        else:
            try:
                # 尝试去数据库中去读取，如果没有读取到就购物车增加一条新信息
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, False)
                c.save()
        #如果是成功就使用json返回数据给HTML   让HTML早在页面上进行一些展示
        product.storenums -= 1  #在添加商品的时候使库存减一
        product.save()
        return JsonResponse({"data": c.productnum, "price": c.productprice, "status": "success"})  #返回总价，便于计算商品的总价格

    elif flag == '1':
               # 将用户的所有的购物车数据全部拿出来
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            #如果没有数量了直接随便返回一个
            return JsonResponse({"data":-2,"status":"error"})

        else:
            try:
                # 尝试去数据库中去读取，如果没有读取到就购物车增加一条新信息
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                #如果购物车中的数量是0了  就执行物理删除，移除购物车
                if c.productnum ==0:
                    c.delete()
                else:
                    c.save()

            except Cart.DoesNotExist as e: #，如果购物车中的这个数量是0，就不能执行，因为上面try不到数据
                return JsonResponse({"data": -2, "status": "error"})
        #如果是成功就使用json返回数据给HTML   让HTML早在页面上进行一些展示
        product.storenums += 1  #在添加商品的时候使库存加1
        product.save()
        return JsonResponse({"data": c.productnum, "price": c.productprice, "status": "success"})
    elif flag =='2':
        carts =Cart.objects.filter(userAccount = user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ""   #在这定义对号，使用它来进行删除DOM元素
        if c.isChose:
            str = "√"
        return JsonResponse({"data":str,"status": "success"})


#做选好了的 视图界面
def saveorder(request):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        return JsonResponse({"data":-1, "status":"error"})

    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose = True)
    if carts.count() == 0:
        return JsonResponse({"data": -1, "status": "error"})

    oid = time.time() + random.randrange(1, 10000)  #随机产生一个随机的订单号
    oid = "%d"%oid   #使用类型转换
    o = Order.createorder(oid,user.userAccount,0)   #进行保存
    o.save()
    for item in carts:   #选中的商品将它进行逻辑删除，将订单号保存
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({"status": "success"})







def mine(request):
    #调用注册后的session，将登录的名字显示到模板上
    username = request.session.get("username","未登录")
    return render(request,'axf/mine.html', {"title":"我的", "username":username})

#登录
from .forms.login import LoginForm
def login(request):
    if request.method =="POST":   #判断是不是POST请求
        f = LoginForm(request.POST)
        if f.is_valid():   #判断是不是字符串
            #信息 格式没什么问题，验证账号和密码的正确性
            # name = f.changed_data["username"]
            pswd = f.cleaned_data["passwd"]
            nameid = f.cleaned_data["username"]
            try:   #如果用户不存在的话  就要使用异常，密码不对，用户不存在，都返回登录界面
                user = User.objects.get(userAccount = nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')


            # 登陆成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')

        else:
            return render(request, 'axf/login.html', {"title": "登录",
                                                      "form":f,
                                                      "error":f.errors})
                                    #如果在表单印证的时候发生错误就将错误提示出来
    else:
        f = LoginForm()   #江上面的表单传进来，如果不对就进行再次渲染空页面

        return render(request, 'axf/login.html', {"title": "登录",
                                                  "form": f,
                                                  })


#注册
import time
import random,os
from django.conf import settings
def register(request):
    if request.method =="POST":
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0

        token = time.time() + random.randrange(1,100000)  #在注册的时候会产生一个token值，各存一个
        userToken = str(token)
        f = request.FILES["userImg"]    #使用files通过name来获取
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")

        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss, userImg, userRank, userToken)
        #将这个人的信息保存全，然后使用save进行保存
        user.save()
        #使用request将session保存起来，username用来做状态保持，token做登录验证
        request.session["username"] = userName
        request.session["token"] = userToken

        return redirect('/mine/')  #注册成功就会主界面

    else:
        return render(request, 'axf/register.html',{"title":"注册"})

#
# 退出登陆
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')



#验证用户名
from django.http import JsonResponse    #y用他去返回json数据
def checkuserid(request):
    userid = request.POST.get("userid")  #通过userid去user的表中去取 数据
    # userid是获取用户的ID
    try:#没有报错是取到数据了，报错了是没有取到数据
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"该用户已经被注册","status":"error"})
                        #将会被ajax 的data接收  返回的是一个字典
    except User.DoesNotExist as e:
        return JsonResponse({"data":"OK", "status":"seccess"})
