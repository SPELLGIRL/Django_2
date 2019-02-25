from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from authapp.models import CustomUser


class UserListView(ListView):
    model = CustomUser
    template_name = 'adminapp/users/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        parent_context = super(UserListView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Users list'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)
