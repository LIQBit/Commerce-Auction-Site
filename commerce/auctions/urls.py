from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("submitcomment/<listing_id>", views.submitcomment, name="submitcomment"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("watchlistpage", views.watchlistpage, name="watchlistpage"),
    path("closebid/<int:listing_id>", views.closebid, name="closebid"),
    path("mywinnings", views.mywinnings, name="mywinnings"),
    path('check_categories/<str:category>', views.check_categories, name='check_category')
  
 
]
