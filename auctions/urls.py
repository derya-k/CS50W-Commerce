from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.newlisting, name="newlisting"),
    path("product/<int:id>", views.product, name="product"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category, name="category"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("delete_watchlist/<int:id>", views.delete_watchlist, name="delete_watchlist"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("my_page", views.my_page, name="my_page"),
    path("sell/<int:id>", views.sell, name="sell"),
     path("close_listing", views.close_listing, name="close_listing"),
]

