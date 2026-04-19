from django.shortcuts import render
import polars as pl
from django.conf import settings
import numpy
import os
import matplotlib.pyplot as plt
import matplotlib
from django.views.generic import ListView
from products.models import Product
from cart.models import Wishlist
from orders.models import Order, OrderItem
import math

matplotlib.use("Agg")


# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
    page_size = 8

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        try:
            page_number = int(self.request.GET.get("page", 1))
        except ValueError:
            page_number = 1

        if page_number < 1:
            page_number = 1

        total_items = queryset.count()
        total_pages = math.ceil(total_items / self.page_size)

        if total_pages > 0 and page_number > total_pages:
            page_number = total_pages

        offset = (page_number - 1) * self.page_size
        end = offset + self.page_size
        page_objects = queryset[offset:end]

        context["products"] = page_objects
        context["current_page"] = page_number
        context["total_pages"] = total_pages
        context["has_previous"] = page_number > 1
        context["has_next"] = page_number < total_pages

        if self.request.user.is_authenticated:
            context["wishlist_ids"] = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product_id", flat=True)
        else:
            context["wishlist_ids"] = []

        return context
    

def dashboard_view(request):
    orders = list(Order.objects.filter(status=Order.status_order.Paid).values())
    df_orders = pl.DataFrame(orders)
    items = list(OrderItem.objects.all().values())
    df_items = pl.DataFrame(items)
    products = list(Product.objects.all().values())
    df_products  = pl.DataFrame(products)
    df_monthly = df_orders.with_columns(
        pl.col("created_at").dt.month().alias("month")
    )
    monthly = (
        df_monthly.group_by("month")
        .agg(pl.sum("total_price").alias("sales"))
        .sort("month")
    )
    df_daily = df_orders.with_columns(
        pl.col("created_at").dt.date().alias("date")
    )
    daily = (
        df_daily.group_by("date")
        .agg(pl.sum("total_price").alias("sales"))
        .sort("date")
    )
    valid_ids = df_products["id"].unique()
    df_items = df_items.filter(pl.col("product_id").is_in(valid_ids))
    df_products_sales = (
        df_items.group_by("product_id")
        .agg(pl.col("quantity").sum().alias("sales_volume"))
        .sort("sales_volume", descending=True)
        )   
    
    df_products_stock = df_products.select(["title", "stock"])
    df_products_sales = (
        df_products_sales
        .join(
            df_products.select(["id", "title"]),
            left_on="product_id",
            right_on="id"
        )
        .select(["title", "sales_volume"])
    )
    monthly_list = monthly["month"].to_list()
    sales_list_monthly = monthly["sales"].to_list()
    daily_list = daily["date"].to_list()
    sales_list_daily = daily["sales"].to_list()
    titles = df_products_sales["title"].to_list()
    sales_volume_list = df_products_sales["sales_volume"].to_list()
    product_list = df_products_stock["title"].to_list()
    stock_product_list = df_products_stock["stock"].to_list()
    
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_list, sales_list_monthly, marker="o")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.savefig("media/charts/monthly_sales.png")
    plt.close()
    
    plt.figure(figsize=(10, 5))
    plt.plot(daily_list, sales_list_daily, marker="s")
    plt.title("Daily sales")
    plt.xlabel("Daily")
    plt.ylabel("Sales")
    plt.savefig("media/charts/daily_sales.png")
    plt.close()
    
    plt.figure(figsize=(14, 6))
    plt.bar(titles, sales_volume_list, color="#1f77b4")
    plt.title("Best Selling Products")
    plt.xlabel("Product")
    plt.ylabel("Sales Volume")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("media/charts/best_selling.png")
    plt.close()
    
    plt.figure(figsize=(10, 5))
    plt.bar(product_list, stock_product_list, color="steelblue")
    plt.xlabel("Product")
    plt.ylabel("Stock")
    plt.title("Product Stock Levels")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("media/charts/stock_levels.png")
    plt.close()
    
    return render(request, "dashboard.html")
    
    
    