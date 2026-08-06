from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post, Category  # ← Category を追加！
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        category_list = Category.objects.all()  # ← 変数名を category_list に変更
        
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'category_list': category_list,     # ← category_list としてテンプレートに渡す
        })


class PostDetailView(View): 
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })

# --- ↓ 追加：カテゴリー別一覧表示ビュー ---
class CategoryView(View):
    def get(self, request, category, *args, **kwargs):
        # 1. 選択されたカテゴリーが存在するか確認し、その投稿を取得
        category_data = get_object_or_404(Category, name=category)
        post_data = Post.objects.filter(category=category_data).order_by('-id')
        
        # 2. ★追加：サイドバー表示用に「全カテゴリーの一覧」を取得する
        category_list = Category.objects.all()
        
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'category_data': category_data, # 選択されたカテゴリー
            'category_list': category_list, # ★追加：全カテゴリーの一覧（サイドバー用）
        })

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_data = form.save(commit=False)
            post_data.author = request.user
            post_data.save()
            return redirect('post_detail', post_data.id)
            
        return render(request, 'app/post_form.html', {
            'form': form
        })
    
class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(instance=post_data)
        return render(request, 'app/post_form.html', {
            'form': form
        })
        
    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(request.POST, request.FILES, instance=post_data)
        if form.is_valid():
            form.save()
            return redirect('post_detail', self.kwargs['pk'])
            
        return render(request, 'app/post_form.html', {
            'form': form
        })          
        
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })
    
    def post(self, request, *args, **kwargs):   
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')