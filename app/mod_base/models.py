from app import db
from app.mod_auth.models import User
from datetime import datetime
now = datetime.now


class Post(db.Document):
    date_created = db.DateTimeField(
        default=now, required=True, verbose_name="Date Created",
        help_text="DateTime when the document was created, localized to the server")
    date_modified = db.DateTimeField(
        default=now, required=True, verbose_name="Date Modified",
        help_text="DateTime when the document was last modified, localized to the server")
    title = db.StringField(
        max_length=255, required=True, verbose_name="Title",
        help_text="Title of the post (255 characters max)")
    author = db.ReferenceField(
        User, required=True, verbose_name="Author",
        help_text="Reference to the User that authored the post")
    content = db.StringField(
        required=True, verbose_name="Content Body",
        help_text="The HTML content of the post")
    slug = db.StringField(
        required=True, verbose_name="Post Slug", regex='([a-z]|[1-9]|-)*',
        help_text="Name of post for use in the url (i.e. my-cool-post)")
    categories = db.ListField(
        db.StringField(
            db_field='category', max_length=255, verbose_name="Category",
            help_text="A category for the post (255 characters max)"),
        verbose_name="Categories", default=list, help_text="A list of categories")
    tags = db.ListField(
        db.StringField(
            db_field='tag', max_length=255, verbose_name="Tag",
            help_text="A tag for the post (255 characters max)"),
        verbose_name="Tags", default=list, help_text="A list of tags for the post")
    published = db.BooleanField(
        required=True, default=False, verbose_name="Published",
        help_text="Whether or not the post is published")
    date_published = db.DateTimeField(
        verbose_name="Date Published",
        help_text="The date when the post is published, localized to the server")
    posted_by = db.ReferenceField(
        User, required=True, default=author,
        verbose_name="Posted By",
        help_text="The User that posted the post, if different from author (i.e. guest author)")

    def clean(self):
        """Update date_modified"""
        self.date_modified = now()

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['title', 'date_created'],
        'ordering': ['-date_created']
    }

    def __repr__(self):
        rep = '%r(title=%r, author=%r, categories=%r, tags=%r, published=%r' %\
            (self.__class__.__name__, self.title, self.author, self.categories,
             self.tags, self.published)

        # excluded if None
        rep += ', date_published=%r' % (self.date_published) \
            if self.date_published else ""
        rep += ', posted_by=%r' % (self.posted_by) if self.posted_by else ""

        # cut down to 100 characters
        if len(self.content) > 100:
            rep += ', content=%r' % (self.content[:97] + "...")
        else:
            rep += ', content=%r' % (self.content)
        return rep