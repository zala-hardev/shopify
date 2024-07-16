from dataclasses import field
from django.contrib import admin
from django.http import HttpResponse
from .models import Customer,Product,Cart,OrderPlaced,WishList,Review,Colors

# to generate pdf
from reportlab.pdfgen import canvas
from reportlab.platypus import Table,TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def download_pdf(self,request,queryset):
  model_name = self.model.__name__
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

  pdf = canvas.Canvas(response,pagesize=letter)
  pdf.setTitle('Invoice')

  headers = [field for field in self.model._meta.fields]
  data = [headers]

  for obj in queryset:
    data_row = [str(getattr(obj,field.name)) for field in self.model._meta.fields]
    data.append(data_row)

  table = Table(data)
  table.setStyle(TableStyle(
    [
    ('BACKGROUND', (0,0), (-1,0), colors.gray),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]
  ))

  canvas_width = 600
  canvas_height = 600

  table.wrapOn(pdf,canvas_width,canvas_height)
  table.drawOn(pdf,40,canvas_height - len(data))

  pdf.save()

  return response

download_pdf.short_description = "Download It"

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display = ('id','customer_name','customer_phone','customer_address','customer_city','customer_state','customer_country')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

  list_display = ('id','product_name','selling_price','discounted_price','description','brand','category','product_quantity','highlight_product_image','front_product_image','back_product_image','rightside_product_image','leftside_product_image','auto_increment_id')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):

  list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):

  list_display = ('id','user','product','quantity','ordered_date','order_status','is_paid','razor_pay_order_id','razor_pay_payment_id','razor_pay_payment_signature')
  actions = [download_pdf]

@admin.register(WishList)
class WishListModelAdmin(admin.ModelAdmin):

  list_display = ('id','user','product','added_at')

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):

  list_display = ('id','user','product','order','ratings','created_at')

@admin.register(Colors)
class ColorsModelAdmin(admin.ModelAdmin):

  list_display = ('id','color_name')


