from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.shortcuts import render, get_object_or_404
from .models import Post


class PostListView(ListView):
   # queryset = Post.published.all() is the same as model = Post
   queryset = Post.published.all()
   context_object_name = 'posts'
   paginate_by = 3
   template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    '''Only works with 'published' articles.
       In Post model in models.py 'unique_for_date' param was added in the 'slug' field-
       - this ensures that there will be only one post with a slug for a given date.
       Raise Error [404 - Not Found] if no object is found.
    '''
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day,)

    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
   # Retrieve post by id
   post = get_object_or_404(Post, id=post_id, status='published')
   if request.method == "POST":
      # Form was submited
      form = EmailPostForm(request.POST)
      if form.is_valid():
         # Form fields passed the validation
         cd = form.cleaned_data
         # ... send email
   else: 
      form = EmailPostForm()
   return render(request, 'blog/post/share.html', {'post': post, 'form': form})


# post_list() is that same as PosrListView()
# def post_list(request):
#    '''Lists all articles. posts = Post.published.all()
#    '''
#    object_list = Post.published.all()
#    paginator = Paginator(object_list, 3) # 3 posts in each page
#    page = request.GET.get('page')

#    try:
#       posts = paginator.page(page)
#    except PageNotAnInteger:
#       # If page is not an integer deliver the first page
#       posts = paginator.page(1)
#    except EmptyPage:
#       # If page is out of range deliver last page of results
#       posts = paginator.page(paginator.num_pages)

#    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
