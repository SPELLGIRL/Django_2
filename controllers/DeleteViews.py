from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from authapp.models import CustomUser
from django.urls import reverse_lazy


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'adminapp/users/delete.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        parent_context = super(UserDeleteView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Delete user'

        return parent_context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class OrderDelete(DeleteView):
    pass
