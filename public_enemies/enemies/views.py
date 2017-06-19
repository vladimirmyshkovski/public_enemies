from django.shortcuts import render, get_object_or_404, redirect
from public_enemies.enemies.models import Enemy
from public_enemies.enemies.forms import EnemyForm, VoteForm
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from secretballot.views import vote
from secretballot.models import Vote
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
# Create your views here.

def only_one_vote(request, content_type, object_id, vote):
    print(Vote.objects.filter(content_type=content_type, token=request.secretballot_token).count())
    return Vote.objects.filter(content_type=content_type, token=request.secretballot_token).count() < 5

class IndexView(generic.ListView):
    template_name = 'enemies/index.html'
    context_object_name = 'enemies'

    def get_queryset(self):
    	print(self.request.secretballot_token)
    	return Enemy.objects.order_by('-total_upvotes')[:15]


class DetailView(generic.DetailView):
    context_object_name = 'enemy'
    template_name = 'enemies/detail.html'

    def get_object(self):
        return get_object_or_404(Enemy, pk=self.kwargs.get("enemy_id"))


class CreateView(generic.CreateView):
    form_class = EnemyForm
    template_name = 'enemies/create.html'
    message = _('Спасибо за Ваш вклад. Враг народа успешно внесён в картотеку!')     

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.avatar = form.cleaned_data['avatar']
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
    	messages.success(self.request, self.message)
    	return reverse('index')
    

class UpVoteView(generic.View):
    model = Enemy
    
    def get_object(self):
        return get_object_or_404(Enemy, pk=self.kwargs.get("enemy_id"))

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.kwargs.get("enemy_id")
        content_type = ContentType.objects.get_for_model(self.model)
        print(only_one_vote(request, content_type, object_id, vote=-1))
        if only_one_vote(request, content_type, object_id, vote=-1):
            vote(request, content_type, object_id, vote=-1)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpVoteView, self).dispatch(request, *args, **kwargs)

class DownVoteView(generic.View):
    model = Enemy

    def get_object(self):
        return get_object_or_404(Enemy, pk=self.kwargs.get("enemy_id"))
    
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.kwargs.get("enemy_id")
        content_type = ContentType.objects.get_for_model(self.model)
        print(only_one_vote(request, content_type, object_id, vote=+1))
        if only_one_vote(request, content_type, object_id, vote=+1):
            vote(request, content_type, object_id, vote=+1)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('index')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DownVoteView, self).dispatch(request, *args, **kwargs)
