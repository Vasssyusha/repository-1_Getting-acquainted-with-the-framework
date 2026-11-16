import uuid
from django.db import models
from django.urls import reverse


class Language(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Язык",
        help_text="Введите язык книги"
    )

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название жанра",
        help_text="Введите жанр книги"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Дата смерти", null=True, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор"
    )
    summary = models.TextField(
        max_length=1000,
        verbose_name="Аннотация",
        help_text="Введите краткое описание книги"
    )
    isbn = models.CharField(
        max_length=13,
        verbose_name="ISBN",
        help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        help_text="Выберите жанр для этой книги"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Язык"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Уникальный ID для конкретного экземпляра во всей библиотеке"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Книга"
    )
    imprint = models.CharField(max_length=200, verbose_name="Издательство")
    due_back = models.DateField(verbose_name="Дата возврата", null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Забронирована'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        verbose_name="Статус",
        help_text='Доступность книги'
    )

    class Meta:
        ordering = ["due_back"]
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"

    def __str__(self):
        return f"{self.id} ({self.book.title})"