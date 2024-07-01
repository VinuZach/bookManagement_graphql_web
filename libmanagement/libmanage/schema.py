import graphene
from graphene_django import DjangoObjectType, DjangoListField

from .models import *


class AuthorDetailsType(DjangoObjectType):
    class Meta:
        model = AuthorDetails
        fields = ("id", "name", "star_rating")


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ("id", "name")


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "author", "availability_status", "genre")


# class AutherDetailsQuery(graphene.ObjectType):
#     all_author_details = graphene.List(AuthorDetailsType)
#
#     def resolve_all_author_details(root, info):
#         return AuthorDetails.objects.all()


class Query(graphene.ObjectType):
    all_authors = DjangoListField(AuthorDetailsType)
    all_genre = DjangoListField(GenreType)
    all_books = DjangoListField(BooksType)
    books_by_author_name = graphene.Field(BooksType, author_name=graphene.String())
    author_by_id = graphene.Field(AuthorDetailsType, id=graphene.Int())

    def resolve_author_by_id(root, info, id):
        return AuthorDetails.objects.get(pk=id)

    def resolve_books_by_author_name(root, info, author_name):
        return Books.objects.get(author__name=author_name)

    def resolve_all_authors(root, info):
        return AuthorDetails.objects.all()


class BooksCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)
        availability_status = graphene.String(required=True)
        genre_id = graphene.Int(required=True)

    create_books = graphene.Field(BooksType)

    @classmethod
    def mutate(cls, root, info, title, author_id, availability_status, genre_id):
        author_details = AuthorDetails.objects.get(id=author_id)
        genre_details = Genre.objects.get(id=genre_id)
        book_details = Books(title=title, author=author_details, availability_status=availability_status,
                             genre=genre_details)
        book_details.save()
        return BooksCreateMutation(create_books=book_details)


class GenreCreateMutation(graphene.Mutation):
    """
    create genre
    """

    class Arguments:
        name = graphene.String(required=True)

    create_genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, name):
        genre = Genre(name=name)
        genre.save()
        return GenreCreateMutation(create_genre=genre)


class AuthorCreateMutation(graphene.Mutation):
    """
    create author
    """

    class Arguments:
        name = graphene.String(required=True)
        star_rating = graphene.Int(required=True)

    create_author = graphene.Field(AuthorDetailsType)

    @classmethod
    def mutate(cls, root, info, name, star_rating):
        author = AuthorDetails(name=name, star_rating=star_rating)
        author.save()
        return AuthorCreateMutation(create_author=author)


class AuthorUpdateMutation(graphene.Mutation):
    """
    update author
    """

    class Arguments:
        id_value = graphene.ID()
        print(id_value)
        name = graphene.String(required=True)
        star_rating = graphene.Int(required=True)

    updated_author = graphene.Field(AuthorDetailsType)

    @classmethod
    def mutate(cls, root, info, id_value, name, star_rating):
        print(id_value)
        author = AuthorDetails.objects.get(id=id_value)
        author.name = name
        author.star_rating = star_rating
        author.save()
        return AuthorUpdateMutation(updated_author=author)


class AuthorDeleteMutation(graphene.Mutation):
    """
    Delete
    """

    class Arguments:
        id_value = graphene.ID()

    delete_author = graphene.Field(AuthorDetailsType)

    @classmethod
    def mutate(cls, root, info, id_value):
        author = AuthorDetails.objects.get(id=id_value)
        author.delete()
        return


class Mutation(graphene.ObjectType):
    delete_author = AuthorDeleteMutation.Field()
    create_author = AuthorCreateMutation.Field()
    update_author = AuthorUpdateMutation.Field()

    create_book = BooksCreateMutation.Field()
    create_genre = GenreCreateMutation.Field()


schema_link = graphene.Schema(query=Query, mutation=Mutation)
