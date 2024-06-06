from django.db import models

class student(models.Model):
    cID = models.AutoField(primary_key=True)
    cName = models.CharField(max_length=20,null=False)
    cSex = models.CharField(max_length=2,default='M',null=False)
    cBirthday = models.DateField(null=False)
    cEmail = models.EmailField(max_length=100,blank=True,default='')
    cPhone = models.CharField(max_length=20,blank=True,default='')
    cAddr = models.CharField(max_length=255,blank=True,default='')

#加盟店下客戶
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    #更新點數時間
    last_updated = models.DateTimeField(auto_now=True)

#加盟店
class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    #camera攝影機ip
    camera_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

#種類:EX:洗衣機,烘碗機等
class Category(models.Model):
    name = models.CharField(max_length=64)

#型號
class Machine(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #型號規格
    model = models.CharField(max_length=100)
    specifications = models.TextField()
    #機器說明
    description = models.TextField()
    #機器圖片
    image_url = models.CharField(max_length=255, blank=True, null=True)  # 圖片路徑或 URL
    #機器狀態:空閒,使用中,維修中
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Maintenance')], default='available')
    created_at = models.DateTimeField(auto_now_add=True)

#訂單 業務
class Order(models.Model):
    #
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #訂單編號
    order_number = models.IntegerField()
    #訂單狀態:進行中,完成,取消
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

#訂單item 業務
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    #數量
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

#購物車 訂單
class ShoppingOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

#購物車 訂單item
class ShoppingItem(models.Model):
    #商品名稱
    name = models.CharField(max_length=100)
    #商品描述
    description = models.TextField()
    #商品價格
    price = models.IntegerField()
    #商品圖片
    image_url = models.CharField(max_length=255, blank=True, null=True)  # 圖片路徑或 URL
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 關聯到 categories 表的主鍵
    created_at = models.DateTimeField(auto_now_add=True)

#購物車 
class ShoppingOrderItem(models.Model):
    shopping_order = models.ForeignKey(ShoppingOrder, on_delete=models.CASCADE)
    shopping_item = models.ForeignKey(ShoppingItem, on_delete=models.CASCADE)
    #數量
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

#交易 
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    #點數型態: 儲值或花費
    type = models.CharField(max_length=20, choices=[('earn', 'Earn'), ('spend', 'Spend')], null=False)
    #描述
    description = models.CharField(max_length=255)
    #建立時間
    created_at = models.DateTimeField(auto_now_add=True)

#通知
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    #訊息
    message = models.CharField(max_length=255)
    #完成時間
    completed_at = models.DateTimeField(null=True, blank=True)
    #刪除時間
    deleted_at = models.DateTimeField(null=True, blank=True)
    #建立時間
    created_at = models.DateTimeField(auto_now_add=True)
#接收0~19洗衣機 0~9洗衣機發訊號 10~19
#接收20~39烘衣機 20~29烘衣機發訊號 30~39烘衣機接訊號
#接收40~59販賣機 40~49販賣機發訊號 50~59販賣機接訊號
#接收60~79洗寵物機 60~69洗寵物機發訊號 70~79
#接收80~99兌換幣機 80~89兌換幣機發訊號 90~99
#接收100~119洗鞋機 100~109洗鞋機發訊號 110~119
#接收120~139洗碗機 120~129洗碗機發訊號 130~139


class MachineUseAdd(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine,on_delete=models.CASCADE) 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)





