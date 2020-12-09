from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login as auth_login
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def registrar_usuario(self, request, *args, **kwargs):
        usuario = User()
        usuario.last_name = request.data['last_name']
        usuario.first_name = request.data['first_name']
        usuario.username = request.data['username']
        usuario.email = request.data['email']
        usuario.set_password(request.data['password'])
        usuario.save()
        grupo = Group.objects.filter(id=1).first()
        usuario.groups.add(grupo)
        # result = UserSerializer(usuario, many=True)
        return Response({'userid': usuario.id, 'name': usuario.first_name, 'lastname': usuario.last_name, 'email': usuario.email, 'username': usuario.username}, status=status.HTTP_200_OK)
        # return Response(result.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def login_usuario(self,request):
        usuario_obtenido = request.data['username']
        pass_obtenida = request.data['password']
        obj_user = authenticate(username=usuario_obtenido, password=pass_obtenida)
        try:
            if obj_user != None:
                auth_login(request, obj_user)
                result = UserSerializer(obj_user, many=False)
                return Response(result.data, status=status.HTTP_200_OK)
                # return Response('hola', status=status.HTTP_200_OK)
            else:
                result = 'Nada'
                return Response(result,status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e)

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def editar_usuario(self, request):
        try:
            usuario = User.objects.filter(id=request.data['usrID']).first()
            usuario.last_name = request.data['last_name']
            usuario.first_name = request.data['first_name']
            usuario.username = request.data['username']
            usuario.email = request.data['email']
            contra = request.data['password']
            if contra != 'd':
                usuario.set_password(contra)
            usuario.save()
            return Response({'userid': usuario.id, 'name': usuario.first_name, 'lastname': usuario.last_name, 'email': usuario.email, 'username': usuario.username}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e)

@api_view(['POST'])
def login_usuario(request):
    usuario_obtenido = request.data['username']
    pass_obtenida = request.data['password']
    obj_user = authenticate(username=usuario_obtenido, password=pass_obtenida)
    try:
        if obj_user != None:
            # auth_login(request, obj_user)
            return Response({'userid': obj_user.id})
            # return Response({'userid': obj_user.id, 'username': obj_user.first_name, 'lastname': obj_user.last_name, 'email': obj_user.email})
            # return Response('hola', status=status.HTTP_200_OK)
        else:
            result = 'Nada'
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(e)