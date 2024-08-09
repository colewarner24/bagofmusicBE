from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, NumberAttribute, MapAttribute

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

    album_id = UnicodeAttribute(null=True)
    title = UnicodeAttribute(null=True)
    artist = UnicodeAttribute()
    date = UnicodeAttribute()
    genres_primary = ListAttribute()
    genres_secondary = ListAttribute()
    rating = NumberAttribute(range_key=True)
    total_ratings = UnicodeAttribute()
    total_reviews = UnicodeAttribute()
    genre_descriptors = ListAttribute()
    spotify_id = UnicodeAttribute(hash_key=True)
    applemusic_id = UnicodeAttribute(null=True)
    soundcloud_id = UnicodeAttribute(null=True)
    bandcamp_id = UnicodeAttribute(null=True)
    youtube_id = UnicodeAttribute(null=True)
    
# Use a paginated scan function to handle large datasets
def paginated_scan(filter_condition, limit):
    scan_kwargs = {}
    last_evaluated_key = None
    while True:
        print("scanning")
        results = Album.scan(**scan_kwargs, filter_condition=filter_condition, limit=limit, last_evaluated_key=last_evaluated_key)
        for item in results:
            yield item
        if results.last_evaluated_key:
            #scan_kwargs['exclusive_start_key'] = results.last_evaluated_key
            last_evaluated_key = results.last_evaluated_key
        else:
            break