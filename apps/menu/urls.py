from django.urls import path
from .views import MenuView

urlpatterns = [
    
    
    #------------------------------------CATEGORIES----------------------------------

    #POST
    path('add-category', MenuView.as_view(action='add_category'), name='add-category'),
    path('put-category', MenuView.as_view(action='update_category'), name='put-category'),
    path('upload-image-category', MenuView.as_view(action='upload_image_category'), name='upload-image-category'),

    #GET
    path('get-categories', MenuView.as_view(action='get_categories'), name='get-categories'),
    
    #DELETE
    path('delete-category/<int:id>', MenuView.as_view(action='delete_category'), name='delete-category'),

    #------------------------------------PROMOTIONS----------------------------------
    #POST
    path('add-promotion', MenuView.as_view(action='add_promotion'), name='add-promotion'),
    path('put-promotion', MenuView.as_view(action='update_promotion'), name='put-promotion'),
    path('upload-image-promotion', MenuView.as_view(action='upload_image_promotion'), name='upload-image-promotion'),

    #GET
    path('get-promotions', MenuView.as_view(action='get_promotions'), name='get-promotions'),
    
    #DELETE
    path('delete-promotion/<int:id>', MenuView.as_view(action='delete_promotion'), name='delete-promotion'),
    
    #------------------------------------PRODUCTS----------------------------------
    path('add-product', MenuView.as_view(action='add_product'), name='add-product'),
    path('put-product', MenuView.as_view(action='update_product'), name='put-product'),
    path('upload-image-product', MenuView.as_view(action='upload_image_product'), name='upload-image-product'),
    
    #GET
    path('get-products', MenuView.as_view(action='get_products'), name='get-products'),
    
    #DELETE
    path('delete-product/<int:id>', MenuView.as_view(action='delete_product'), name='delete-product'),
    
    
   
    
]
