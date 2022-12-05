## Why did I created it ?

I just created this because I was a bit lazy and I don't want to search for all the songs in apple music, and sometimes the song isn't available in there, so I used the Spotify API beacause the catalog is greater (and also I don't want to pay 100$ to use the apple one) so I found way to have the apple musics link for free 😎


# Usage

Songs-to-platforms is a Python library for creating links to "hyperlinks" it leverages the platform ToneDen with its free accounts to create links to various platforms, Spotify, Apple Music, iTunes, etc...

In the library is available a Spotify Client that can interact with their API in a basic manner, in the code is configured for searching for songs/tracks, (because what we need for the campaign in ToneDen is the track's link)

with the modules, some functions can extract information from youtube videos, from comments or the timestamps, I recommend using the timestamps, as there have been in my experience the format of the string more consistent, while the comments can change from different users, I purposely made the different functions separate and not a continuous because maybe there could be some cleaning to be done

### make sure to have this row format before creating the links:

(is assuming that this is a pandas.DataFrame)

    '{artist_name}' | '{song_name}' | '{artist_name} // {song_name}'


### or in case the artist's name is not available:

    '-' | '{songs_name}' | '- // {song_name}'


there's no need to create the third column yourself there's a function that I created, `format_for_link`






### import the modules:
```python
from songs import links
from titles import format_for_link, get_songs_from_comments
from SpotifyAPI import SpotifyClient

# for cleaning the DataFrame if necesarily
import pandas as pd
```

### obtain the data:

```python
url_youtube = 'https://www.youtube.com/watch?v=2vhWfMSr4YM&t=2321s'
songs_df = get_songs_from_comments(url_youtube)
```

### Instance the Spotify Client

```python
client_ID = 'not so secret'
client_secret = 'super secret'
client = SpotifyClient(client_ID, client_secret)
```

### Prepare the data

make sure you have the following format:

`{artist_name} | {song's_name}`

-------------

`'-' | {song's_name}` <span style="color:#5399ba"> *if the artist is unknown* </span>


```python
songs_df = format_for_link(songs_df)
```



### Once finished
we can implement the function

```python
songs_df['link'] = songs_df['link'].apply(links, client = client)
```

if there's multiple matches in the search the program will need our attention to choose the one we want, once we have the track's link we can use it directly and it would be fine, but if you are a apple music or iTunnes user you may want to follow some more steps.


### The Bot

I created a little bot that takes the spotify links to ToneDen and creates the campign in seconds, you will need to create an account in their platform and give the password and the email for the platform (I advice to use a dumb email that you doesn't use)

in order to work you will need to have installed the browser driver, in this case I used the firefox browser if you want to change it you can change it in the module of the Bot.

```python
with Bot(teardown=True, email= 'something@email.com', password= '5UP3R_53CR37'
    ) as bot:

    # we pass the dataframe with the spotify links
    bot.create_links(data_frame)

```
I implemented the  teardown parameter in case someone wanted to use the with statement but didn't want to close the browser sesion

## Contributing

Pull requests are welcome, for implementing more funcionality of dealing with bugs.
