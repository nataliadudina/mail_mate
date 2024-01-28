from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from blog.models import Article


class BlogListView(ListView):
    # Displays a list of published articles
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'
    paginate_by = 6
    extra_context = {'page_title': 'Mailing Blog', 'title': 'Mailing Blog'}

    # Only retrieves published articles for the view
    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(publication=Article.Status.PUBLISHED).order_by('id')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = context['object_list']
        return context


class ArticleDetailView(DetailView):
    # Shows the details of a single article
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Mailing Blog: read'
        context['page_title'] = page_title
        context['title'] = self.object.title
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)  # Retrieves the article
        self.object.views_count += 1  # Increment the views count
        self.object.save(update_fields=['views_count'])   # Saves only views_count field
        return self.object


class ArticleFormMixin:
    # Validates the form and sets the article's slug
    def form_valid(self, form):
        if form.is_valid():
            article = form.save(commit=False)
            article.slug = slugify(article.title)

            image = form.cleaned_data['image']
            if image:
                article.image = image
            article.save()
            return super().form_valid(form)


class ArticleCreateView(UserPassesTestMixin, ArticleFormMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'publication', 'image')
    extra_context = {'page_title': 'Mailing Blog: write', 'title': 'Writing New Post'}

    def test_func(self):
        # User must be in 'content-manager' group
        return self.request.user.groups.filter(name='content-manager').exists()


class ArticleUpdateView(UserPassesTestMixin, ArticleFormMixin, UpdateView):
    # User must pass certain checks to update an article
    model = Article
    fields = ('title', 'content', 'publication', 'image')
    extra_context = {'page_title': 'Mailing Blog: edit', 'title': 'Updating the Post'}

    # Checks if the user is allowed to update the article
    def test_func(self):
        article = self.get_object()
        # User must be in 'content-manager' group
        return self.request.user.groups.filter(name='content-manager').exists()


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_delete.html'
    extra_context = {'page_title': 'Mailing Blog', 'title': 'Delete the Post'}
    success_url = reverse_lazy('list')

    def test_func(self):
        article = self.get_object()
        # User must be in 'content-manager' group
        return self.request.user.groups.filter(name='content-manager').exists()
