from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from GaleriaDuende.models import Image
from Logic.DAO.SingletonDAO import singleton

@singleton
class AdmStore:
    def newProduct(self, name, description, price, quantity, image):
        product  = Product()
        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity
        product.image = image
        product.save()

    def updateProduct(self,product, name, description, price, quantity, image):
        product = Product.objects.get(id=product)
        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity
        if (image != None) :
            product.image = image
        product.save() 

    def removeProduct(self, product):
        producto = Product.objects.get(id = product)
        producto.delete()

    def addToCart(self, cliente, product):
        producto = Product.objects.get(id = product)
        carrito = ShoppingCart.objects.get(client = cliente)
        carrito.save()
        carrito.products.add(producto.id)
        carrito.save()
    
    def removeFromCart(self, cliente, product):
        carrito = ShoppingCart.objects.get(client = cliente)
        producto = Product.objects.get(id=product)
        carrito.products.remove(producto.id)
        carrito.save()

    def buy(self, distrito, purchaseDate, voucher, user, description):
        compra = Purchase()
        carritos = ShoppingCart.objects.all()
        productosCarrito = []
        total = 0
        items = 0
        carritoUser = None
        for cart in carritos:
            if (cart.client == user):
                carritoUser = cart
                productosCarrito = cart.products.all()
                
        #------------------------------------------------------
        compra.client = user
        compra.distrito = Distrito.objects.get(name = distrito)
        compra.deliveryDate = purchaseDate
        compra.voucher = voucher
        compra.state = "PENDIENTE"
        compra.description = description
        compra.save()
        #------------------------------------------------------
        for p in productosCarrito:
            p.quantity = p.quantity - 1
            p.save()
            carritoUser.products.remove(p.id)
            carritoUser.save()
            compra.products.add(p.id)
            total = total + p.price
            items += 1

        compra.price = total
        compra.items = items
        compra.save()
        return compra.id

    def payPurchase(self, purchaseName, voucher, deliveryDate):
        purchase = Purchase.objects.get(name=purchaseName)
        purchase.voucher = voucher
        purchase.deliveryDate = deliveryDate
        purchase.save()
    
    def newProvincia(self, name):
        provincia = Provincia()
        provincia.name = name
        provincia.save()
    
    def newCanton(self, nameProvincia, nameCanton):
        provincia = Provincia.objects.get(name=nameProvincia)
        canton = Canton()
        canton.name = nameCanton
        canton.provincia = provincia
        canton.save()

    def newDistrito(self, nameCanton, nameDistrito):
        distrito = Distrito()
        distrito.name = nameDistrito
        distrito.canton = Canton.objects.get(name=nameCanton)
        distrito.save()

    def deleteProvincia(self, nameCatalogo):
        provincia = Provincia.objects.get(id=nameCatalogo)
        provincia.delete()

    def deleteCanton(self, nameCatalogo):
        provincia = Canton.objects.get(id=nameCatalogo)
        provincia.delete()
    
    def deleteDistrito(self, nameCatalogo):
        provincia = Distrito.objects.get(id=nameCatalogo)
        provincia.delete()

#-----------------------------------------------------------------------------------
class Provincia(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------
class Canton(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=CASCADE)

    def __str__(self):
        return self.name 

#-----------------------------------------------------------------------------------
class Distrito(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    canton = models.ForeignKey(Canton, on_delete=CASCADE)

    def __str__(self):
        return self.name 

#-----------------------------------------------------------------------------------
class Address(models.Model):
    location = models.CharField(max_length=1024, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, on_delete=CASCADE)

    def __str__(self):
        return self.location

#-----------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image =  models.ImageField(upload_to = "Productos", null=True)
    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------
class ShoppingCart(models.Model):
    client = models.CharField(max_length=100,  null=True, blank=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.client
#-----------------------------------------------------------------------------------
class Voucher(models.Model):
    image = models.CharField(max_length=50, null=True, blank=True)

#-----------------------------------------------------------------------------------
class Purchase(models.Model):
    client = models.CharField(max_length=1024, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, on_delete=CASCADE,null=True, blank=True)
    voucher = models.ImageField(upload_to = "Voucher", null=True)
    products =  models.ManyToManyField(Product)
    items = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    deliveryDate = models.DateTimeField(default=datetime.now, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    
#-----------------------------------------------------------------------------------






