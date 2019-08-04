from rest_framework import generics
from .models import Insumos
from .serializers import InsumosSerializer, TokenSerializer, UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from .decorators import validate_request_data
# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



class ListInsumosView(generics.ListAPIView):

    queryset = Insumos.objects.all()
    serializer_class = InsumosSerializer
    permission_classes = (permissions.IsAuthenticated,)


    #@validate_request_data
    def post(self, request, *args, **kwargs):
        un_insumo = Insumos.objects.create(
            name=request.data["name"],
            machine=request.data["machine"]
        )
        return Response(
            data=InsumosSerializer(un_insumo).data,
            status=status.HTTP_201_CREATED
        )


class InsumosDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Insumos.objects.all()
    serializer_class = InsumosSerializer

    def get(self, request, *args, **kwargs):
        try:
            un_insumo = self.queryset.get(pk=kwargs["pk"])
            return Response(InsumosSerializer(un_insumo).data)
        except Insumos.DoesNotExist:
            return Response(
                data={
                    "message": "Insumo con id: {} no existe en inventario".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            un_insumo = self.queryset.get(pk=kwargs["pk"])
            serializer = InsumosSerializer()
            updated_insumo = serializer.update(un_insumo, request.data)
            return Response(InsumosSerializer(updated_insumo).data)
        except Insumos.DoesNotExist:
            return Response(
                data={
                    "message": "Insumo con id: {} no existe en inventario".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            un_insumo = self.queryset.get(pk=kwargs["pk"])
            un_insumo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Insumos.DoesNotExist:
            return Response(
                data={
                    "message": "Insumo con id: {} no existe en inventario".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class LoginView(generics.CreateAPIView):
	#Logeo
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            #login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
	#Registro
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "Todos los datos de usuario son requeridos para el registro"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )
