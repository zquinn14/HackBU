from lxml import html
import requests
import re
import random
import sys

ARTIST_URL = "http://www.metrolyrics.com/{artist}-alpage-{n}.html"
SONG_URL = "http://www.metrolyrics.com/{title}-lyrics-{artist}.html"
SONG_RE = r'http://www\.metrolyrics\.com/(.*)-lyrics-(.*)\.html'


def slugify(string):
    return string.replace(' ', '-').lower()


def deslugify(string):
    return string.replace('-', ' ').title()


class Song(object):
    """An object that represents a song, whose lyrics can be retrieved."""

    def __init__(self, title=None, artist=None, url=None):
        """
        Create a song.
        You can EITHER provide a URL for the song lyrics, OR provide the
        lower-case hyphenated song title and artist.  If both are provided, the
        URL is preferred.
        """
        self._lyrics = None
        if url is not None:
            self._url = url
            self.title, self.artist = re.match(SONG_RE, url).groups()
        elif title is not None and artist is not None:
            self.title = title
            self.artist = artist
            self._url = SONG_URL.format(
                title=slugify(title),
                artist=slugify(artist),
            )
        else:
            raise ValueError('Must provide either title & artist or URL.')

        self.title = deslugify(self.title)
        self.artist = deslugify(self.artist)

    def load(self):
        """Load the lyrics from MetroLyrics."""
        page = requests.get(self._url)
        # Forces utf-8 to prevent character mangling
        page.encoding = 'utf-8'

        tree = html.fromstring(page.text)
        lyric_div = tree.get_element_by_id('lyrics-body-text')
        verses = [c.text_content() for c in lyric_div if c.get('id') != "mid-song-discussion"]
        self._lyrics = '\n\n'.join(verses)

        self._lyrics = self._lyrics.replace("\n", "<br/>")

        return self

    @property
    def lyrics(self):
        if self._lyrics is None:
            self.load()
        return self._lyrics

    def format(self):
       return self.lyrics

    def __repr__(self):
        return 'Song(title=%r, artist=%r)' % (self.title, self.artist)


class Artist(object):
    """
    An object that represents an artist, and can get you their songs.
    Pass into the constructor the "name" of the artist.  Generally, this is the
    lower case name with spaces replaced by hyphens, and punctuation removed.
    I don't really provide any utilities for searching for this name.  If you
    just Google the artist + " lyrics", you'll probably get their MetroLyrics
    page, and so you can get the artist's "name" from that.
    """

    def __init__(self, name):
        self._songs = None
        self.name = slugify(name)

    def load(self, verbose=False):
        """
        Load the list of songs.
        Note that this only loads a list of songs that this artist was the main
        artist of.  If they were only featured in the song, that song won't be
        listed here.  There is a list on the artist page for that, I just
        haven't added any parsing code for that, since I don't need it.
        """
        self._songs = []
        page_num = 1
        total_pages = 1

        while page_num <= total_pages:
            if verbose:
                print('retrieving page %d' % page_num)
            page = requests.get(ARTIST_URL.format(artist=self.name,
                                                  n=page_num))
            tree = html.fromstring(page.text)
            song_rows_xp = r'//*[@id="popular"]/div/table/tbody/tr'
            songlist_pagination_xp = r'//*[@id="main-content"]/div[1]/'\
                                     'div[2]/p/span/a'

            rows = tree.xpath(song_rows_xp)
            for row in rows:
                song_link = row.xpath(r'./td/a[contains(@class,"title")]')
                assert len(song_link) == 1
                self._songs.append(Song(url=song_link[0].attrib['href']))

            total_pages = len(tree.xpath(songlist_pagination_xp))
            page_num += 1
        return self

    @property
    def songs(self):
        if self._songs is None:
            self.load()
        return self._songs

    def __repr__(self):
        return 'Artist(%r)' % self.name


if __name__ == '__main__':
    artist_name = input("Artist name ")
    song_name = input("Song name ")

    if len(sys.argv) > 1:
        artist_name = sys.argv[1]

    if len(sys.argv) > 2:
        song_name = sys.argv[2]

    if song_name:
        song = Song(
            title=song_name,
            artist=artist_name,
        )
    else:
        artist = Artist(artist_name)
        song = random.choice(artist.songs)

    print(song.format())