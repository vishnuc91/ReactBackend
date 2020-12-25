from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from todo.models import *
from django.db import transaction


# Create your views here.

class CreateBucket(APIView):

    def get(self, request):
        buckets = []
        bucket = Bucket.objects.all()
        for buck in bucket:
            data = {"id":buck.id, "name": buck.name, "create_time": buck.datetime.time(), "create_date": buck.datetime.date()}
            buckets.append(data)
        return Response({"message": "succesful", "data": buckets})

    @transaction.atomic()
    def post(self, request):
        name = request.POST.get("name")
        sid = transaction.savepoint()
        if name != "":

            bucket = Bucket(name=name)
            bucket.save()
            transaction.savepoint_commit(sid)
            return Response({"message": "New Bucket Created with {name}".format(name=name)})
        else:
            transaction.savepoint_rollback(sid)
            return Response({"message": "error"})


class CreateTodo(APIView):

    def get(self, request):
        bucket_id = request.GET.get("bucket_id")
        todos = []
        if Bucket.objects.filter(id=bucket_id).exists():
            todo = Todo.objects.filter(bucket=bucket_id)
            for to in todo:
                data = {"bucket_name": to.bucket.name, "bucket_id": to.bucket.id, "todo_name": to.name,
                        "date": to.target.date(), "time": to.target.time(), "todo_id": to.id}
                todos.append(data)
            return Response({"message": "succesful", "data": todos})
        else:
            return Response({"message": "unsuccesful", "data": "Invalid parameter"})

    def post(self, request):
        bucket_id = request.POST.get("bucket_id")
        name = request.POST.get("name")
        date_time = request.POST.get("date_time")
        sid = transaction.savepoint()
        if bucket_id!="":
            if Bucket.objects.filter(id=bucket_id).exists():
                if name != "" or date_time!="":
                    bucket = Bucket.objects.get(id=bucket_id)
                    todo = Todo(bucket=bucket, name=name, target=date_time)
                    todo.save()
                    transaction.savepoint_commit(sid)
                    return Response({"message": "New Bucket Created with {name}".format(name=name)})
                else:
                    transaction.savepoint_rollback(sid)
                    return Response({"message": "error"})
            else:
                return Response({"message": "Invalid Bucket"})
        else:
            return Response({"message": "Invalid Bucket"})


