from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import os
import zipfile
from ftplib import FTP
import xmltodict, json
from django.db import connection
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Download
from .serializers import DownloadSerializer, DownloadSerializer2


def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE article_download_id_seq RESTART WITH 1")
        row = connection.commit()

    return row


def index(request):
    jsonData_list = Download.objects.order_by('-created_at').all()
    count_list = Download.objects.all().count()
    paginator = Paginator(jsonData_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'count_list': count_list}
    )


def download(request):
    Download.objects.all().delete()
    my_custom_sql(1)
    ftp = FTP('ftp.zakupki.gov.ru')
    ftp.login('free', 'free')
    dirName = '/fcs_regions/Kaliningradskaja_obl/notifications/currMonth/'
    ftp.cwd(dirName)
    files_list = ftp.nlst()
    count = 0
    t = 1
    for i in files_list:
        static = os.path.join('./static/', i)
        ftp.retrbinary("RETR %s" % i, open(static, 'wb').write)
        fzip = zipfile.ZipFile(f'{static}')
        fzip.extractall(f'./static/{count}')
        for root, dirs, files in os.walk(f"./static/{count}"):
        # Прочитать содержимое
            for f in os.scandir(f"./static/{count}"):
                if f.is_file() and f.path.split('.')[-1].lower() == 'xml':
                    with open(f.path, 'r') as xmlfile:
                        o = xmltodict.parse(xmlfile.read())
                        data = (json.dumps(o, ensure_ascii=False))
                        t += 1
                        Download.objects.create(jsonData=data)

        fzip.close()
        count += 1

    return redirect('index')


class ArticleView(APIView):

    def get(self, request):
        if request.GET.get('articles', None):
            articles = Download.objects.filter(id=request.GET.get('articles'))
        else:
            articles = Download.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = DownloadSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        article = request.data.get('article')
        # Create an article from the above data
        serializer = DownloadSerializer2(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "New post '{}' created successfully".format(article_saved.jsonData)})

    def put(self, request, pk):
        saved_article = get_object_or_404(Download.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = DownloadSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({
            "success": "Article '{}' updated successfully".format(article_saved.jsonData)
        })

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Download.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)
