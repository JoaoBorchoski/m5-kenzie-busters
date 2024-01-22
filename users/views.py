from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from users.models import User
from users.permissions import MyCustomPermission

from django.forms.models import model_to_dict


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, req):
        user = User.objects.get(email="lucira_buster@kenziebuster.com")
        user.delete()
        return Response("deletado")

    def post(self, req):
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserViewDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, req, user_id):
        user_req = model_to_dict(req.user)
        try:
            user = UserSerializer(User.objects.get(pk=user_id))
            user = user.data

            if user_req["is_employee"] == True:
                return Response(user)
            elif user_req["email"] != user["email"]:
                return Response(
                    {"detail": "Authentication credentials were not provided."}, 403
                )
            return Response(user)

        except User.DoesNotExist:
            return Request("message: user not found.")

    def patch(self, req, user_id):
        user_req = model_to_dict(req.user)
        try:
            user = User.objects.get(pk=user_id)
            if user_req["is_employee"] == True:
                serializer = UserSerializer(user, req.data, partial=True)
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data)
            elif user_req["email"] != model_to_dict(user)["email"]:
                return Response(
                    {"detail": "Authentication credentials were not provided."}, 403
                )
            serializer = UserSerializer(user, req.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)

        except User.DoesNotExist:
            return Request("message: user not found.")
