from rest_framework import serializers
from libra.models import Book, MyBook
from users.models import Reader


class BookSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    action_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'status', 'action_url']

    def get_status(self, obj):
        user = self.context['request'].user
        if user.role == 'RDR':
            reader = Reader.objects.filter(user=user).first()
            if reader:
                return 'взята' if MyBook.objects.filter(book=obj, reader=reader,
                                                        return_date__isnull=True).exists() else 'доступна'
        return 'доступна'

    def get_action_url(self, obj):
        request = self.context['request']
        status = self.get_status(obj)
        if status == 'взята':
            return request.build_absolute_uri(f"/api/books/{obj.id}/return_book/")
        else:
            return request.build_absolute_uri(f"/api/books/{obj.id}/borrow/")


class MyBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    days_borrowed = serializers.SerializerMethodField()

    class Meta:
        model = MyBook
        fields = ['id', 'book', 'borrow_date', 'days_borrowed']

    def get_days_borrowed(self, obj):
        from django.utils import timezone
        return (timezone.now() - obj.borrow_date).days


class BorrowBookSerializer(serializers.Serializer):
    pass
