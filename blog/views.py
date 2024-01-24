from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from blog.models import Article


class ArticleCreateView(CreateView):    # LoginRequiredMixin
    model = Article
    fields = ('title', 'content', 'image')
    extra_context = {'page_title': 'Mailing Blog: write', 'title': 'Writing New Post'}
    success_url = reverse_lazy('list')

    # Validates the form and sets the article's slug and author
    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save(commit=False)  # Prepare the article without saving to DB
            new_article.slug = slugify(new_article.title)  # Generate a slug from the title
            # new_article.author = self.request.user  # Set the current user as the author
            new_article.save()   # Save the article to the DB

            # If an image is provided, attach it to the article
            image = form.cleaned_data['image']
            if image:
                new_article.image = image
                new_article.save()

            return super().form_valid(form)  # Call the superclass method to handle redirection


class BlogListView(ListView):
    # Displays a list of published articles
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'
    paginate_by = 9
    extra_context = {'page_title': 'Mailing Blog', 'title': 'Mailing Blog'}

    # Only retrieves published articles for the view
    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(publication=Article.Status.PUBLISHED)


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
        self.object.save()  # Save the updated article
        return self.object


class ArticleUpdateView(UpdateView):    # UserPassesTestMixin,
    # User must pass certain checks to update an article
    model = Article
    fields = ('title', 'content', 'image', 'publication')
    extra_context = {'page_title': 'Mailing Blog: edit', 'title': 'Updating the Post'}
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        if form.is_valid():
            edited_article = form.save(commit=False)
            edited_article.slug = slugify(edited_article.title)
            edited_article.save()

            return super().form_valid(form)

    def get_success_url(self):
        return reverse('view', args=[self.object.slug])

    # Checks if the user is allowed to update the article
    # def test_func(self):
    #     article = self.get_object()
    #     # User must be in 'content-manager' group or the author of the article
    #     return self.request.user.groups.filter(name='content-manager').exists() or self.request.user == article.author


class ArticleDeleteView(DeleteView):    # UserPassesTestMixin,
    model = Article
    template_name = 'blog/article_delete.html'
    extra_context = {'page_title': 'Mailing Blog', 'title': 'Delete the Post'}
    success_url = reverse_lazy('list')

    # def test_func(self):
    #     article = self.get_object()
    #     # User must be in 'content-manager' group or the author of the article to delete it
    #     return self.request.user.groups.filter(name='content-manager').exists() or self.request.user == article.author
