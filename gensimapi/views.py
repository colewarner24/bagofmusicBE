import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Album
from .word2vec_helper import get_similar_words
from django.views.decorators.http import require_POST
import traceback, sys

@require_POST
def query_albums(request):
    try:
        data = json.loads(request.body)
        words = data.get('words', [])
        
        if not words:
            return JsonResponse({'error': 'words list is required'}, status=400)

        # Collect albums that match any of the provided descriptors
        descriptors = get_similar_words("models/descriptors.json", words)
        
        # Create a dictionary to store albums and their match counts
        album_scores = {}
        print(descriptors)

        for descriptor in descriptors:
            albums = Album.scan(
                Album.genre_descriptors.contains(descriptor)
            )
            for album in albums:
                print("here")
                print(album)
                print(album.genre_descriptors)
                print("also here")
                if album.spotify_id not in album_scores: #change spotify_id later to album_id
                    # Initialize score and add album to dictionary
                    album_scores[album.spotify_id] = {'album': album, 'score': 0}
                    
                    score = sum(1 for d in album.genre_descriptors if d in descriptors)
                    
                    if score >= 2: #threshold for consideration
                        album_scores[album.spotify_id]['score'] += score
                        
        # Remove albums with a score of 0
        album_scores = {k: v for k, v in album_scores.items() if v['score'] > 0}
                
        # Sort albums based on the number of matching descriptors (score)
        sorted_albums = sorted(album_scores.values(), key=lambda x: x['score'], reverse=True)[:10]
       
        len(sorted_albums)
        for album in sorted_albums:
            print(album['album'].title, album['score'])
        # Prepare the response
        response = [album['album'].attribute_values for album in sorted_albums]
        return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})
    except json.JSONDecodeError:
        print("Invalid JSON format")
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        trace=traceback.extract_tb(sys.exc_info()[2])
        # Add the event to the log
        output ="Error in the server: %s.\n" % (e)
        output+="\tTraceback is:\n"
        for (file,linenumber,affected,line)  in trace:
            output+="\t> Error at function %s\n" % (affected)
            output+="\t  At: %s:%s\n" % (file.replace(" ", "%"),linenumber)
            output+="\t  Source: %s\n" % (line)
        output+="\t> Exception: %s\n" % (e)
        print(output)
        return JsonResponse({'error': str(output)}, status=500)