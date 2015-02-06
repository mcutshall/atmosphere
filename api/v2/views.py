import django_filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.decorators import detail_route
from core.models import Tag, Project, Application as Image, Provider, Identity, Quota, Allocation, Volume, \
    Instance, InstanceAction, VolumeAction, ProviderType, PlatformType, ProviderMachine, \
    ApplicationBookmark as ImageBookmark, Group, Size
from core.models.user import AtmosphereUser
from .serializers import TagSerializer, UserSerializer, ProjectSerializer, ImageSerializer, ProviderSerializer, \
    IdentitySerializer, QuotaSerializer, AllocationSerializer, VolumeSerializer, InstanceSerializer, \
    InstanceActionSerializer, VolumeActionSerializer, ProviderTypeSerializer, PlatformTypeSerializer, \
    ProviderMachineSerializer, ImageBookmarkSerializer, SizeSerializer, SizeSummarySerializer
from core.query import only_current
from rest_framework import permissions


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        method = self.request.method
        if method == 'DELETE' or method == 'PUT':
            self.permission_classes = (IsAdminUser,)

        return super(viewsets.ModelViewSet, self).get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AtmosphereUser.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('email',)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        return Project.objects.filter(only_current(), owner__name=user.username)

    @detail_route()
    def instances(self, *args, **kwargs):
        project = self.get_object()
        self.get_queryset = super(viewsets.ModelViewSet, self).get_queryset
        self.queryset = project.instances.get_queryset()
        self.serializer_class = InstanceSerializer
        return self.list(self, *args, **kwargs)

    @detail_route()
    def volumes(self, *args, **kwargs):
        project = self.get_object()
        self.get_queryset = super(viewsets.ModelViewSet, self).get_queryset
        self.queryset = project.volumes.get_queryset()
        self.serializer_class = VolumeSerializer
        return self.list(self, *args, **kwargs)


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_fields = ('created_by__username', 'tags__name')
    search_fields = ('name', 'description')


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'options', 'trace']

    def get_permissions(self):
        method = self.request.method
        if method == 'DELETE' or method == 'PUT':
            self.permission_classes = (IsAdminUser,)

        return super(viewsets.GenericViewSet, self).get_permissions()

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        group = Group.objects.get(name=user.username)
        return group.providers.filter(only_current(), active=True)

    @detail_route()
    def sizes(self, *args, **kwargs):
        provider = self.get_object()
        self.get_queryset = super(viewsets.ModelViewSet, self).get_queryset
        self.queryset = provider.size_set.get_queryset()
        self.serializer_class = SizeSummarySerializer
        return self.list(self, *args, **kwargs)


class IdentityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer

    def get_queryset(self):
        """
        Filter identities by current user
        """
        user = self.request.user
        group = Group.objects.get(name=user.username)
        providers = group.providers.filter(only_current(), active=True)
        return user.identity_set.filter(provider__in=providers)


class QuotaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer


class AllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer


class VolumeFilter(django_filters.FilterSet):
    min_size = django_filters.NumberFilter(name="size", lookup_type='gte')
    max_size = django_filters.NumberFilter(name="size", lookup_type='lte')

    class Meta:
        model = Volume
        fields = ['provider__id', 'min_size', 'max_size']


class VolumeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer
    filter_class = VolumeFilter

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        return Volume.objects.filter(only_current(), created_by=user)


class InstanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    filter_fields = ('created_by__id',)

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        return Instance.objects.filter(only_current(), created_by=user)


class InstanceActionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = InstanceAction.objects.all()
    serializer_class = InstanceActionSerializer


class VolumeActionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = VolumeAction.objects.all()
    serializer_class = VolumeActionSerializer


class ProviderTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = ProviderType.objects.all()
    serializer_class = ProviderTypeSerializer


class PlatformTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = PlatformType.objects.all()
    serializer_class = PlatformTypeSerializer


class ProviderMachineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = ProviderMachine.objects.all()
    serializer_class = ProviderMachineSerializer


class ImageBookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = ImageBookmark.objects.all()
    serializer_class = ImageBookmarkSerializer

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        return ImageBookmark.objects.filter(user=user)


class SizeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

    def get_queryset(self):
        """
        Filter projects by current user
        """
        user = self.request.user
        group = Group.objects.get(name=user.username)
        providers = group.providers.filter(only_current(), active=True)
        return Size.objects.filter(only_current(), provider__in=providers)
