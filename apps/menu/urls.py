from django.urls import path
from .views import MenuView

urlpatterns = [
    #POST
    path('add-category', MenuView.as_view(action='add_category'), name='add-category'),
    path('put-category', MenuView.as_view(action='update_category'), name='put-category'),
    path('add-product', MenuView.as_view(action='add_product'), name='add-product'),
    path('add-promotion', MenuView.as_view(action='add_promotion'), name='add-promotion'),
    path('upload-image-category', MenuView.as_view(action='upload_image_category'), name='upload-image-category'),

    #GET
    path('get-categories', MenuView.as_view(action='get_categories'), name='get_categories'),
   
    #DELETE
    path('delete-category/<int:id>', MenuView.as_view(action='delete_category'), name='delete-category'),
]
