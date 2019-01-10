import boto3
from django.http import HttpResponse


def home(request):
    return serve_s3_file("triptracks", "client/index.html")


def home_js(request):
    return serve_s3_file("triptracks", "client/main.js")


def favicon(request):
    return serve_s3_file("triptracks", "client/favicon.ico", False)


def serve_s3_file(bucket, path, utf8=True):
    print("serving ", path)
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, path)
    content = obj.get()['Body'].read()
    if utf8:
        content = content.decode('utf-8')
    return HttpResponse(content)


