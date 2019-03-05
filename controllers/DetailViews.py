from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from authapp.models import CustomUser


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'adminapp/users/read.html'

    def get_context_data(self, **kwargs):
        parent_context = super(UserDetailView, self).get_context_data(**kwargs)
        parent_context['title'] = 'User view'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


class OrderRead(DetailView):
    pass
