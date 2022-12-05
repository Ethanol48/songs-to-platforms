from itertools import islice
from youtube_comment_downloader import *
import pandas as pd
import re
import pytube
downloader = YoutubeCommentDownloader()

def get_songs_from_comments(url, n: int = 25, sep: str = '-', enumerated: bool = True ):
    """
    This functions returns a dataframe of the songs obtained from the comments
    of the video

    the line containing the titles should have the following format:

    if enumarated:
    (time) 00. artist - song

    if not:
    (time) artist - song

    Parameters
    ---------------
    url: url of the youtube video

    Opcional Params
    ---------------
    sep: character in the comments separating the author's name
    from the song's name

    enumerated: boolean, if True is interpret that the songs in the comments are
    numbered 01. , 02. , 03. , ... ect

    n: number of comments to load from the comment section by default is 25

    """

    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)

    def arreglar_nums(num):
        if 'k' in num or 'K' in num:
            num = num.replace('K','')
            num = num.replace('k','')
            num = num.replace(',','')
            num = num.replace('.','')
            num = num.replace(' ', '')
            num = int(num)
            return num * 1000
        else:
            if '.' in num:
                return 0
            return int(num)

    lst = []
    for comment in islice(comments, n +1):
        lst.append(comment)

    coms = pd.DataFrame(lst).drop(columns = [
        'time_parsed','heart','cid','reply','channel','time','photo','author'
        ]).copy()

    coms['votes'] = coms['votes'].apply(arreglar_nums)
    coms = coms.sort_values('votes',ascending= False).reset_index(drop=True)

    titles = []
    ti = []
    for n in coms.text:
        n = n.splitlines()

        for i in n:
            if len(re.findall(
                '\d{1,2}[:]\d{2}[:]\d{1,}|\d{1,2}[:]\d{2}', i)) != 0:

                tmp = i.replace(re.findall(
                    '\d{1,2}[:]\d{2}[:]\d{1,}|\d{1,2}[:]\d{2}', i
                    )[0],'')

                if tmp.startswith('()'):
                    tmp = tmp.replace('() ','',1)

                if tmp.startswith('[]'):
                    tmp = tmp.replace('[] ','',1)

                if enumerated:
                    if len(re.findall('\d{2}', tmp)) != 0:
                        tmp = tmp.replace(re.findall('\d{2}', tmp)[0],'')

                    if tmp.startswith('.'):
                        tmp = tmp.replace('. ','',1)


                ti.append(tmp)

        titles.append(ti)

    tmp = []
    for _ in titles:
        for i in _:
            a = i.strip().split(sep)

            if len(a) == 1:
                a = [None, a[0]]
                tmp.append(a)

            else:
                a = [a[0].strip(), a[1].strip()]
                tmp.append(a)

    df_songs = pd.DataFrame(tmp, columns= ['artist', 'song'])

    return df_songs.drop_duplicates()

def get_songs_time_stamps(url, sep: str = '-'):

    """
    This functions returns a dataframe of the songs obtained from the timestamps
    of the video

    the line containing the titles should have the following format:

    {time_stamp} artist {sep} song


    Parameters
    ---------------
    url: url of the youtube video
    n: number of comments to load from the comment section


    Opcional Params
    ---------------
    separator: character in the comments separating the author's name
    from the song's name

    """

    video = pytube.YouTube(url)

    time_stamps = []

    for i in video.description.split('\n'):
        if len(re.findall(
            '\d{1,2}[:]\d{2}[:]\d{1,}|\d{1,2}[:]\d{2}', i)
            ) != 0:

            tmp = i.replace(re.findall(
                '\d{1,2}[:]\d{2}[:]\d{1,}|\d{1,2}[:]\d{2}', i)[0],'')

            time_stamps.append(tmp.replace(' - ', '', 1))


    df_titles = pd.DataFrame(time_stamps, columns= ['title'])
    return df_titles

def format_for_link(df):

    tmp_df = pd.DataFrame(columns=['link'])
    lst = []

    for row in df.values:
        if row[0] == None:
            row[0] = '-'
            lst.append([f"{row[0].strip()} // {row[1].strip()}"])

        else:
            lst.append([f"{row[0].strip()} // {row[1].strip()}"])

    tmp_df = pd.DataFrame(lst, columns=['link'])
    final_df = pd.concat([df, tmp_df], axis = 1)

    return final_df.fillna('-').copy()
