from django.urls import path
from .views import VentureView

urlpatterns = [
    #POST
    path('set-venture', VentureView.as_view(action='set_venture'), name='set-venture'),
    path('set-image-venture', VentureView.as_view(action='set_image_venture'), name='set-image-venture'),
    path('new-branch', VentureView.as_view(action='new_branch'), name='new-branch'),
    path('put-branch', VentureView.as_view(action='update_branch'), name='put-branch'),
    path('add-images-branch', VentureView.as_view(action='add_branch_images'), name='add-images-branch'),
    
    #GET
    path('get-images-branch/<int:id>', VentureView.as_view(action='get_branch_images'), name='get-images-branch'),
    path('get-branch/<int:id>', VentureView.as_view(action='get_branch'), name='get-branch'),
    path('get-venture-information/', VentureView.as_view(action='get_venture_info'), name='get-venture-information'),
   
    #DELETE
    path('delete-branch-image/<int:id>', VentureView.as_view(action='delete_branch_photo'), name='delete-branch-image'),
    path('delete-branch/<int:id>', VentureView.as_view(action='delete_branch'), name='delete-branch'),
]
