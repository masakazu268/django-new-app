from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'app/index.html', {
            'post_data': post_data
        })

class PostDetailView(View): 
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })
        
class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        # フォームに POST と FILES を両方渡す
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_data = form.save(commit=False) # まだ保存しない
            post_data.author = request.user     # ログイン中の作者をセット
            post_data.save()                    # タイトル・本文・画像を1回で保存！
            return redirect('post_detail', post_data.id)
            
        return render(request, 'app/post_form.html', {
            'form': form
        })
    
class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # ModelForm の場合は instance に既存データを渡します
        form = PostForm(instance=post_data)
        return render(request, 'app/post_form.html', {
            'form': form
        })
        
    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # instance を指定することで上書き更新になります
        form = PostForm(request.POST, request.FILES, instance=post_data)
        if form.is_valid():
            form.save() # 画像の差し替えも含めて1回で更新！
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