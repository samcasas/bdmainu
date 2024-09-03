from django.urls import path
from .views import MenuView

urlpatterns = [
    #POST
    path('add-category', MenuView.as_view(action='add_category'), name='add-category'),
    path('add-product', MenuView.as_view(action='add_product'), name='add-product'),
    path('add-promotion', MenuView.as_view(action='add_promotion'), name='add-promotion'),
    
    #GET
    #path('add-product', MenuView.as_view(action='get_branch_images'), name='get-images-branch'),
   
    #DELETE
    #path('add-product', MenuView.as_view(action='delete_branch_photo'), name='delete-branch-image'),
]
