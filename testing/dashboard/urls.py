from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.get_all_products),
    path("users", views.get_all_users),
    path("users/<id>", views.get_all_products),
    path("delete/<id>" , views.delete_by_id),
    path("update/<id>", views.update_by_id),
    path('recommended/<int:user_id>', views.recommendation_page, name='recommended_product'),
    path('productviewed/<product_id>', views.product_viewed, name='product_viewed'),
    path('', views.login_page),
    path('register/', views.register_page),
    path('logout', views.logout_page),
]