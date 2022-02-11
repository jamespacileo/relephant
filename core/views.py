from django.shortcuts import render

# Create your views here.


from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

class RPGJSRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        path = self.request.path
        return f'/static{path}'

        # article = get_object_or_404(Article, pk=kwargs['pk'])
        # article.update_counter()
        # return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)