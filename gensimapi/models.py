from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, NumberAttribute, UnicodeSetAttribute

import os

class Album(Model):
    class Meta:
        table_name = 'rym_collection'  # Replace with your DynamoDB table name
        if os.getenv("EB_DEV") or True: # remove
            region = 'us-east-1'
            aws_access_key_id=os.getenv("DYNAMO_SECRET_KEY")
            aws_secret_access_key=os.getenv("DYNAMO_SECRET_ACCESS_KEY")
        else:
            region = 'us-east-1'  # Replace with your AWS region
            host = "http://localhost:8000"

    album_id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute(range_key=True)
    artist = UnicodeAttribute()
    date = UnicodeAttribute()
    genres_primary = ListAttribute()
    genres_secondary = ListAttribute()
    rating = NumberAttribute()
    total_ratings = UnicodeAttribute()
    total_reviews = UnicodeAttribute()
    genre_descriptors = ListAttribute()
    spotify_id = UnicodeAttribute(null=True)
    applemusic_id = UnicodeAttribute(null=True)
    soundcloud_id = UnicodeAttribute(null=True)
    bandcamp_id = UnicodeAttribute(null=True)
    youtube_id = UnicodeAttribute(null=True)