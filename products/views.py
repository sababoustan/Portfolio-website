from .models import Product
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from comments.models import Comment
from comments.forms import CommentForm


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/shop-product-basic.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = Comment.objects.filter(
            product=product, 
            is_active=True, 
            parent__isnull=True
            )
        comment_form = CommentForm()
        context.update({
            "comments": comments,
            "comment_form": comment_form
            })
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.get_object()
            comment.is_active = False
            comment.save()
            messages.success(
            request,
            "کامنت شما با موفقیت ثبت شد و پس از بررسی منتشر خواهد شد"
            )
        return redirect(request.path)
        

class ProductSearchView(ListView):
    template_name = "products/search.html"
    model = Product
    context_object_name = "products"
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        if search:
            return Product.objects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(slug__icontains=search)
            )
        else:
            return Product.objects.filter(is_active=True)
            