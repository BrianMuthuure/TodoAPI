from functools import partial
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from.models import Todo
from.serializers import TodoSerializer



class TodoListApiView(APIView):
    # Add permission to check if the user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    # list all the todos
    def get(self, request, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Todo.objects.filter(user=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create todo
    def post(self, request, **kwargs):
        """
        Create the Todo with the given todo data
        """
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    '''
    Helper method to get the object with given todo_id, and user_id
    '''
    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None
    # retrieve
    def get(self, request, todo_id, **kwargs):
        """
        Retrieves Todo with given todo_id
        """
        instance = self.get_object(todo_id, request.user.id)
        if not instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update
        
    def put(self, request, todo_id, **kwargs):
        instance = self.get_object(todo_id, request.user.id)
        if not instance:
            return Response(
                {"res": "Object with this todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST

            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self, request, todo_id, **kwargs):
        """
        Delete the todo item with given todo_id if exists
        """

        instance = self.get_object(todo_id, request.user.id)
        if not instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )