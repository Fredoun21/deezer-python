"""
Module to implement the various types of resources that
can be found in the API.
"""


class Resource:
    """
    Base class for any resource.

    It is mainly responsible of passing a reference to the client
    to this class when instantiated, and transmit the json data into
    attributes
    """

    def __init__(self, client, json):
        self._fields = tuple(json.keys())
        self.client = client
        for key in json:
            setattr(self, key, json[key])

    def __repr__(self):
        name = getattr(self, "name", getattr(self, "title", None))
        if name is not None:
            return "<{}: {}>".format(self.__class__.__name__, str(name))
        return super().__repr__()

    def asdict(self):
        """
        Convert resource to dictionary
        """
        result = {}
        for key in self._fields:
            value = getattr(self, key)
            if isinstance(value, list):
                value = [i.asdict() if isinstance(i, Resource) else i for i in value]
            if isinstance(value, Resource):
                value = value.asdict()
            result[key] = value
        return result

    def get_relation(self, relation, **kwargs):
        """
        Generic method to load the relation from any resource.

        Query the client with the object's known parameters
        and try to retrieve the provided relation type. This
        is not meant to be used directly by a client, it's more
        a helper method for the child objects.
        """
        # pylint: disable=E1101
        return self.client.get_object(self.type, self.id, relation, self, **kwargs)

    def iter_relation(self, relation, **kwargs):
        """
        Generic method to iterate relation from any resource.

        Query the client with the object's known parameters
        and try to retrieve the provided relation type. This
        is not meant to be used directly by a client, it's more
        a helper method for the child objects.
        """
        # pylint: disable=E1101
        index = 0
        while 1:
            items = self.get_relation(relation, index=index, **kwargs)
            yield from items

            if len(items) == 0:
                break
            index += len(items)

    def get_artist(self):
        """
        :returns: the :mod:`Artist <deezer.resources.Artist>` of the resource
        :raises TypeError: if the object is not album or track
        """
        # pylint: disable=E1101
        if not isinstance(self, (Album, Track)):
            raise TypeError("Is neither an Album or a Track")
        return self.client.get_artist(self.artist.id)


class Album(Resource):
    """
    To work with an :deezer-api:`album object <album>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_tracks(self, **kwargs):
        """
        Get a list of album's tracks.

        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("tracks", **kwargs)

    def iter_tracks(self, **kwargs):
        """
        Iterate album's tracks.

        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.iter_relation("tracks", **kwargs)


class Artist(Resource):
    """
    To access an :deezer-api:`artist object <artist>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_top(self, **kwargs):
        """
        Get the top tracks of an artist.

        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("top", **kwargs)

    def get_related(self, **kwargs):
        """
        Get a list of related artists.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.get_relation("related", **kwargs)

    def iter_related(self, **kwargs):
        """
        Iterate related artists.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.iter_relation("related", **kwargs)

    def get_radio(self, **kwargs):
        """
        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("radio", **kwargs)

    def get_albums(self, **kwargs):
        """
        Get a list of artist's albums.

        :returns: list of :mod:`Album <deezer.resources.Album>` instances
        """
        return self.get_relation("albums", **kwargs)

    def iter_albums(self, **kwargs):
        """
        Iterate artist's albums.

        :returns: list of :mod:`Album <deezer.resources.Album>` instances
        """
        return self.iter_relation("albums", **kwargs)


class Genre(Resource):
    """
    To access an :deezer-api:`genre object <genre>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_artists(self, **kwargs):
        """
        Get all artists for a genre.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.get_relation("artists", **kwargs)

    def iter_artists(self, **kwargs):
        """
        Iterate artists for a genre.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.iter_relation("artists", **kwargs)

    def get_radios(self, **kwargs):
        """
        Get all radios for a genre.

        :returns: list of :mod:`Radio <deezer.resources.Track>` instances
        """
        return self.get_relation("radios", **kwargs)

    def iter_radios(self, **kwargs):
        """
        Iterate radios for a genre.

        :returns: list of :mod:`Radio <deezer.resources.Track>` instances
        """
        return self.iter_relation("radios", **kwargs)


class Track(Resource):
    """
    To access an :deezer-api:`track object <track>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_album(self):
        """
        :returns: the :mod:`Album <deezer.resources.Album>` instance
        """
        return self.client.get_album(self.album.id)


class User(Resource):
    """
    To access an :deezer-api:`user object <user>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_albums(self, **kwargs):
        """
        Get user's favorite albums.

        :returns: list of :mod:`Album <deezer.resources.Album>` instances
        """
        return self.get_relation("albums", **kwargs)

    def iter_albums(self, **kwargs):
        """
        Iterate user's favorite albums.

        :returns: list of :mod:`Album <deezer.resources.Album>` instances
        """
        return self.iter_relation("albums", **kwargs)

    def get_tracks(self, **kwargs):
        """
        Get user's favorite tracks.

        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("tracks", **kwargs)

    def iter_tracks(self, **kwargs):
        """
        Iterate user's favorite tracks.

        :returns: list of :mod:`Track <deezer.resources.Track>` instances
        """
        return self.iter_relation("tracks", **kwargs)

    def get_artists(self, **kwargs):
        """
        Get user's favorite artists.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.get_relation("artists", **kwargs)

    def iter_artists(self, **kwargs):
        """
        Iterate user's favorite artists.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.iter_relation("artists", **kwargs)

    def get_playlists(self, **kwargs):
        """
        Get user's public playlists.

        :returns: list of :mod:`Playlist <deezer.resources.Playlist>` instances
        """
        return self.get_relation("playlists", **kwargs)

    def iter_playlists(self, **kwargs):
        """
        Iterate user's public playlists.

        :returns: list of :mod:`Playlist <deezer.resources.Playlist>` instances
        """
        return self.iter_relation("playlists", **kwargs)


class Playlist(Resource):
    """
    To access an :deezer-api:`playlist object <playlist>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """


class Comment(Resource):
    """
    To access an :deezer-api:`comment object <comment>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """


class Radio(Resource):
    """
    To access an :deezer-api:`radio object <radio>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    def get_tracks(self, **kwargs):
        """
        Get first 40 tracks in the radio

        :returns: list of  :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("tracks", **kwargs)

    def iter_tracks(self, **kwargs):
        """
        Iterate tracks in the radio

        :returns: list of  :mod:`Track <deezer.resources.Track>` instances
        """
        return self.iter_relation("tracks", **kwargs)


class Chart(Resource):
    """
    To access an :deezer-api:`chart object <chart>`.

    All the fields documented on Deezer are accessible by as class attributes.
    """

    type = "chart"

    id = 0

    def get_tracks(self, **kwargs):
        """
        :returns: list of  :mod:`Track <deezer.resources.Track>` instances
        """
        return self.get_relation("tracks", **kwargs)

    def iter_tracks(self, **kwargs):
        """
        Iterate tracks in the radio

        :returns: list of  :mod:`Track <deezer.resources.Track>` instances
        """
        return self.iter_relation("tracks", **kwargs)

    def get_albums(self, **kwargs):
        """
        :returns: the :mod:`Album <deezer.resources.Album>` instance
        """
        return self.get_relation("albums", **kwargs)

    def iter_albums(self, **kwargs):
        """
        Iterate artist's albums.

        :returns: list of :mod:`Album <deezer.resources.Album>` instances
        """
        return self.iter_relation("albums", **kwargs)

    def get_artists(self, **kwargs):
        """
        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.get_relation("artists", **kwargs)

    def iter_artists(self, **kwargs):
        """
        Iterate artists for a genre.

        :returns: list of :mod:`Artist <deezer.resources.Artist>` instances
        """
        return self.iter_relation("artists", **kwargs)

    def get_playlists(self, **kwargs):
        """
        :returns: list of :mod:`Playlist <deezer.resources.Playlist>` instances
        """
        return self.get_relation("playlists", **kwargs)

    def iter_playlists(self, **kwargs):
        """
        Iterate playlist for a genre.

        :returns: list of :mod:`Playlist <deezer.resources.Playlist>` instances
        """
        return self.iter_relation("playlists", **kwargs)
