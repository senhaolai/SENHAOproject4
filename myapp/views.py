from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.utils import timezone
from django.db.models import Sum

#-----------------------------------------------------------------------------#
#-------------------- 2024/06/05 新增作業的CODE--------------------------------#
#-----------新增HTML allprice.html,index.html,usedetails.html-----------------#
#-----------------------------------------------------------------------------#

def index(request):

    # 在此接收加盟主的id  ,  先預設為2  , 之後應為從客戶前端登入後取得登入帳號的id
    resultList = Machine.objects.filter(store=2).order_by("id")
    store_name = Store.objects.filter(id=2).values("name")
    name = store_name[0]["name"]
    # (if not resultList) 檢查 resultList 是否為空
    if not resultList:
        status = False
    data_count = len(resultList)
    print(data_count)
    return render(request,"index.html",locals())


@csrf_exempt
def createItem(request):
    try:
        if request.method == "POST":
            store_id = request.POST["store_id"]
            machine_id = request.POST["machine_id"]
            user_id= request.POST["user_id"]
            price = request.POST["price"]
            created_at= timezone.now()
        elif request.method == "GET":
            store_id = request.GET["store_id"]
            machine_id = request.GET["machine_id"]
            user_id= request.GET["user_id"]
            price = request.GET["price"]
            created_at= timezone.now()
    except :
        return HttpResponse("輸入資料不完整")
    try:
        # 获取 Store 和 Machine 实例
        store = Store.objects.get(id=store_id)
        machine = Machine.objects.get(id=machine_id)
        user = User.objects.get(id=user_id)

        add = MachineUseAdd(store=store, machine=machine, price=price, user=user)
        add.save()
        return HttpResponse("True")
    except:
        return HttpResponse("存入資料失敗")


def allprice(request, id=None):
        try:
            machine = MachineUseAdd.objects.filter(machine=id).values().order_by("created_at")
            total_price = machine.aggregate(total_price=Sum('price'))['total_price'] or 0
            trade_count = len(machine)
            store_id = machine[0]["store_id"]
            store = Store.objects.get(id=store_id)
            store_name = store.name
            machine_list = list(machine)
            print(total_price)
            status = True
        # (if not machine_list) 檢查 machine_list 是否為空
            if not machine_list:
                status = False
            return render(request,"allprice.html",locals())
            # return HttpResponse(52)
        except:
            return HttpResponse("您無此機台")
        
def usedetails(request, id=None):
        try:
            machine = MachineUseAdd.objects.filter(machine=id).values().order_by("created_at")
            total_price = machine.aggregate(total_price=Sum('price'))['total_price'] or 0
            user_list = [data['user_id'] for data in machine]
            users = User.objects.filter(id__in=user_list)
            usernames_list = [user.username for user in users]
            trade_count = len(machine)
            store_id = machine[0]["store_id"]
            store = Store.objects.get(id=store_id)
            store_name = store.name
            machine_list = list(machine)
            print(usernames_list)
            combined_data = zip(usernames_list, machine_list)
            status = True
        # (if not machine_list) 檢查 machine_list 是否為空
            if not machine_list:
                status = False
            return render(request,"usedetails.html",locals())
            # return HttpResponse(52)
        except:
            return HttpResponse("您無此機台")

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#







