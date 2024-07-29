from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from libra.models import Book, MyBook
from .permissions import IsReader
from .serializers import BookSerializer, MyBookSerializer, BorrowBookSerializer
from django.utils import timezone


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsReader]

    def get_serializer_class(self):
        if self.action == 'borrow' or self.action == 'return_book':
            return BorrowBookSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        reader = request.user.reader
        if MyBook.objects.filter(book=book, reader=reader, return_date__isnull=True).exists():
            return Response({"detail": "У вас уже есть эта книга."}, status=status.HTTP_400_BAD_REQUEST)
        MyBook.objects.create(book=book, reader=reader)
        return Response({"detail": "Книга взята."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        reader = request.user.reader
        mybook = MyBook.objects.filter(book=book, reader=reader, return_date__isnull=True).first()
        if mybook:
            mybook.return_date = timezone.now()
            mybook.save()
            return Response({"detail": "Книга возвращена."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "У вас нет этой книги."}, status=status.HTTP_400_BAD_REQUEST)


class MyBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MyBookSerializer
    permission_classes = [IsReader]

    def get_queryset(self):
        if hasattr(self.request.user, 'reader'):
            return MyBook.objects.filter(reader=self.request.user.reader, return_date__isnull=True)
        return MyBook.objects.none()

    def list(self, request, *args, **kwargs):
        if not hasattr(request.user, 'reader'):
            return Response({"detail": "User is not a reader."}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
