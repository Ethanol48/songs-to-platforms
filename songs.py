from youtube_comment_downloader import *
import pandas as pd
import requests
from urllib.parse import urlencode
from IPython.display import clear_output
import time
import re

downloader = YoutubeCommentDownloader()

def links(row, client):
    """
    This function is ment to be be use in a Pandas DataFrame, to parse through
    a column with the following format; '{artist} // {song}' or '- // {song}' in
    the case of the artist being unknown, separating each element with ' // '
    one space.

    The function is configured in case of the column artist are shared with more
    than one artist, will work, in case of multiple artist, the function
    divides de artists and makes two searches, first with the first artist then
    with the second artist, both searches with the song's name

    In case of multiple results, the user is presented with a table with the
    results and are asked to chose the desired song, in case of not finding the
    result wanted there's an option of choosing none of the results

    The function



    Params
    ----------

    row: DataFrame row
    client: Spotify client, object containing a access_token, in case of not
            being valid for depassing the time alowed, the function checks the
            client automatically, if after that the access_token is not valid
            would result in diferent outputs specifying what's wrong.

    Output
    ----------

    The output is a string of the link to the song in the spotify platform

    """

    def check_pattern(row):
        pattern = re.compile(r".* // .*")

        if pattern.match(row) == None:
            pattern = False
        else:
            pattern = True

        if pattern is False:
            raise TypeError(
        "\n\nthe row doesn't have the correct format, the required format is:\
        \n\n'artist_name // song_name' \n\nor in case of unknown artist:   \
        \n\n'- // song_name' \
        \n\nCheck the function 'format_for_link' in the module 'titles'"
        )

    def obtain_songs(R, dictio: dict, by_artist: bool,
            by_song: bool, special: bool = False
        ):

        lst2 = []

        for track_obj in R.json()['tracks']['items']:

            artis = []
            if by_artist == True:
                lst2.append(track_obj)

            if special == True:
                lst2.append(track_obj)

            else:
                for ar in track_obj.get('artists'):
                    artis.append(ar.get('name'))

                if len(artis) == 1:
                    artis = artis[0]

                    if dictio['artist'].casefold() in artis.casefold() \
                        and dictio['song'].casefold() \
                            in track_obj.get('name').casefold():

                        lst2.append(track_obj)

                else:
                    artis_tmp = []
                    for l in artis:
                        artis_tmp.append(l.casefold())

                    if dictio['artist'].casefold() in artis_tmp \
                        and dictio['song'].casefold() \
                            in track_obj.get('name').casefold():

                        lst2.append(track_obj)

        if len(lst2) == 0:
            return  ':('

        if len(lst2) == 1:
            return lst2[0]['external_urls']['spotify']


        if len(lst2) > 1:

            tmp = []

            for track in lst2:
                if len(track['artists']) > 1:
                    tmp2 = []

                    for artista in track['artists']:
                        tmp2.append(artista['name'])

                    artist = ' // '.join(tmp2)

                else:
                    artist = track['artists'][0]['name']

                song = track['name']
                url = track['external_urls']['spotify']
                tmp.append([artist,song,url])

            df_elegir = pd.DataFrame(tmp, columns = ['artists','songs','url'])



            # checks for the case of only finding one song
            one_song = df_elegir.copy()
            one_song.drop_duplicates(inplace=True, subset= ['artists','songs'])
            one_song = one_song.reset_index(drop=True)

            if len(one_song) == 1:
                return df_elegir.loc[0,'url']

            # drop duplicates
            df_elegir.drop_duplicates(inplace=True, subset= ['artists','songs'])
            df_elegir = df_elegir.reset_index(drop=True)

            # chose row of the information about the search for each case
            if by_song == True and by_artist == False:
                filling = pd.DataFrame(
                    {'artists': ['-'],
                    'songs': ['search by artist'],
                    'url': ['puto el que lea']
                    }, index= [f'{df_elegir.shape[0]}'])
                line = '\tsearching by Song'

            if by_song == False and by_artist == True:
                filling = pd.DataFrame(
                    {'artists': ['-'],
                    'songs': ['None'],
                    'url': ['puto el que lea']
                    }, index= [f'{df_elegir.shape[0]}'])
                line = '\tsearching by Artist'

            if by_song == True and by_artist == True:
                filling = pd.DataFrame(
                    {'artists': ['-'],
                    'songs': ['search by song'],
                    'url': ['puto el que lea']
                    }, index= [f'{df_elegir.shape[0]}'])
                line = '\tsearching by Artist and Song'

            if special == True:
                filling = pd.DataFrame(
                    {'artists': ['-'],
                    'songs': ['None'],
                    'url': ['puto el que lea']
                    }, index= [f'{df_elegir.shape[0]}'])
                line = "\tsearching by Song (we only have the song's name)"

            # append a row whit information about the search
            df_elegir = pd.concat([df_elegir,filling])


            print(

        f"""
        There is a small problem, the program found {df_elegir.shape[0]} results,
        from the table select the song you want to store

        insert the index of the row (0-{df_elegir.shape[0] - 1})

        """
            )

            print('\t  id           artists                      song           ')
            print('\t------  ------------------------ --------------------------')

            for index, row in df_elegir.iterrows():

                if str(index) == str(df_elegir.shape[0] - 1):
                    print('\t-----------------------------------------------------------')
                    print(line)
                    print('\t-----------------------------------------------------------')

                print(f"\t   {index}  |  {row['artists']}  |  {row['songs']}")

            time.sleep(0.2)



            indx = input(f' inserta el index del row (0-{df_elegir.shape[0] - 1})')


            clear_output(wait=False)

            if (int(indx) + 1)  == df_elegir.shape[0]:
                return  ':('

            else:
                return df_elegir.loc[int(indx),'url']

    def sort_results(pr_dictio):

        # search by song and artist
        request = hacer_request(client, pr_dictio)

        if ultimate_artist_name != '-':

            response = obtain_songs(request, pr_dictio, by_artist = True, by_song= True)

        elif ultimate_artist_name == '-':
            # if we don't have the artist name it will do a search by the songs,
            # in the table should show no more option to keep searching

            response = obtain_songs(request, pr_dictio, by_artist = False, by_song= True, special = True)
            return response


        if response == ':(':

            # search by song
            tmp_dictio = pr_dictio
            tmp_dictio['artist'] = ''

            request = hacer_request(client, tmp_dictio)

            response = obtain_songs(request, pr_dictio, by_song = True, by_artist= False)

            if response == ':(':

                # search by artist
                tmp_dictio = pr_dictio
                tmp_dictio['song'] = ''
                tmp_dictio['artist'] = ultimate_artist_name

                request = hacer_request(client, tmp_dictio)
                response = obtain_songs(request, pr_dictio, by_song= False, by_artist = True)

                return response

            else:
                return response

        else: return response

    def hacer_request(client, dictionario):

        search_url = 'https://api.spotify.com/v1/search?'
        headers = {
            'Authorization': f'Bearer {client.access_token}'
        }
        if dictionario['song'] == '':
            data = urlencode({'q': f"artist:{dictionario['artist']}", 'type': 'track'})

        if dictionario['artist'] == '-':
            data = urlencode({'q': f"{dictionario['song']}", 'type': 'track'})

        else:
            data = urlencode({'q': f"{dictionario['song']} artist:{dictionario['artist']}", 'type': 'track'})

        lookup_url = f'{search_url}{data}'
        r = requests.get(lookup_url, headers = headers)

        return r

    check_pattern(row)

    row = row.split(' // ')
    dictio = {'artist':row[0], 'song': row[1]}
    Artist_ok = True

    if '&&' in dictio['artist']:
        Artist_ok = False

    ultimate = dictio
    ultimate_artist_name = dictio['artist']

    if Artist_ok == False:

        # más de un artista
        results = []
        for i in dictio['artist'].split(' && '):
            tmp = links(' // '.join([i,dictio['song']]), client)
            results.append(tmp)

        if ':(' in results and len(results) == 1:
            return ':('

        if ':(' in results and len(results) > 1:
            no_index = results.index(':(')

            if no_index == 0:
                return results[1]
            elif no_index == 1:
                return results[0]

        return ' | '.join(results)

    elif Artist_ok == True:

        Req = hacer_request(client, dictio)

        if Req.status_code == 401:
            client.check()
            Req = hacer_request(client, dictio)

        if Req.status_code == 403:
            return 'Error with the connection with the API'

        if Req.status_code == 429:
            return "the API can't deliver in the moment"

        if Req.status_code == 200:

            return sort_results(dictio)
