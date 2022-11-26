create table if not exists genres (
genre_id integer primary key,
genre_name VARCHAR not null
);
create table if not exists artists (
artist_id integer primary key,
artist_name VARCHAR not null
);
create table if not exists genres_artists (
genre_id integer references genres(genre_id),
artist_id integer references artists(artist_id),
constraint pk primary key (genre_id, artist_id)
);
create table if not exists albums (
album_id integer primary key,
album_name VARCHAR not null,
album_year integer check(album_year > 0)  not null
);
create table if not exists artists_albums (
artist_id integer references artists(artist_id),
album_id integer references albums(album_id),
constraint pk_2 primary key (artist_id, album_id)
);
create table if not exists tracks (
track_id integer primary key,
track_name VARCHAR not null,
track_length integer check(track_length > 0) not null,
album_id integer references albums(album_id)
);
 create table if not exists compilations (
 compilation_id integer primary key,
 compilation_name VARCHAR not null,
 compilation_year integer check(compilation_year > 0)  not null
 );
create table if not exists tracks_compilations (
track_id integer references tracks(track_id),
compilation_id integer references compilations(compilation_id),
constraint pk_3 primary key (track_id, compilation_id)
);