from datetime import timedelta

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from secret.models import Secret
from secret.paginators import SecretPaginator
from secret.serializers import SecretSerializer
from secret.tasks import burning_secret

class SecretListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = SecretPaginator
    serializer_class = SecretSerializer

    def get_queryset(self):
        return Secret.objects.filter(owner_id=self.request.user.pk)


class SecretGenerateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SecretSerializer
    queryset = Secret.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = "ЗАПОМНИ, после прочтения секрета он будет сожжен," \
                  "secret_key можно использовать только ОДИН раз"

        secret_pk = serializer.data.get('pk')
        date_of_burning = serializer.data.get('date_of_burning')
        test_date = '2023-11-08 15:40:00'



        return Response(
            {
            'secret_key': serializer.data.get('secret_key'),
            'VARNING': message,
            },
            status=status.HTTP_201_CREATED
        )


class SecretRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SecretSerializer

    def get_queryset(self):
        return Secret.objects.filter(owner_id=self.request.user.pk)


class SecretDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SecretSerializer

    def get_queryset(self):
        return Secret.objects.filter(owner_id=self.request.user.pk)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name_secret = instance.name_secret
        self.perform_destroy(instance)
        message = f"'Secret {name_secret} deleted successfully."
        return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)



class ReadSecretRetrieveView(generics.RetrieveAPIView):
    serializer_class = SecretSerializer
    queryset = Secret.objects.all()
    lookup_field = 'secret_key'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if not instance.is_reader:
            instance.is_reader = True
            instance.delete()

        return Response(serializer.data.get('secret'))
