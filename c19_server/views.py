from c19_server.models import Form, UserID, User
from c19_server.serializers import FormSerializer, UserIDSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions, viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin


# Create your views here.
class FormViewSet(viewsets.ModelViewSet, NestedViewSetMixin):
    """
    Menyediakan fungsi 'Create', 'Retrieve', 'Update', dan 'Destroy'
    untuk form pendataan
    """
    serializer_class = FormSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Form.objects.filter(userid__owner=self.request.user)

    def perform_create(self, serializer):
        (param1, param2, param3, param4) = self.request.POST.get('gejala_demam', False), \
                                           self.request.POST.get('usia', False), \
                                           self.request.POST.get('kontak', False), \
                                           self.request.POST.get('aktivitas', False)
        score = 0
        if param1:
            score += 3
        if param2:
            score += 1
        if param3:
            score += 2
        if param4:
            score += 1
        if score >= 5:
            return serializer.save(kategori=3, userid_id=self.kwargs['parent_lookup_userid'])
        elif score >= 3:
            return serializer.save(kategori=2, userid_id=self.kwargs['parent_lookup_userid'])
        elif score < 3:
            return serializer.save(kategori=1, userid_id=self.kwargs['parent_lookup_userid'])


class UserIDViewSet(viewsets.ModelViewSet, NestedViewSetMixin):
    """
    Menyediakan fungsi 'Create', 'Retrieve', 'Update', dan 'Destroy'
    untuk form identitas pengguna
    """
    def get_queryset(self):
        return UserID.objects.filter(owner=self.request.user)

    serializer_class = UserIDSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Menyediakan fungsi 'list' dan 'detail' untuk user (device)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

