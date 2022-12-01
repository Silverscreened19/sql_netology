insert into artists(artist_id, artist_name)
values(1, 'Avicii'), 
(2, 'Placebo'),
(3, 'Depeche mode'),
(4, 'The Weeknd'),
(5, 'The Röyksopp'),
(6, 'Swedish House Mafia'),
(7, 'blink-182'),
(8, 'Low Roar'),
(9, 'Armin van Buuren'),
(10, 'David Bowie'),
(11, 'Kygo');


insert into genres (genre_id, genre_name)
values(1, 'EDM'),
(2, 'Rock'),
(3, 'Indie-Rock'),
(4, 'R&B'),
(5, 'Pop-punk');

insert into albums(album_id, album_name, album_year)
values(1, 'Avīci (01)', 2017),
(2, 'Sleeping with ghosts', 2003),
(9, 'Songs of Faith and Devotion', 1993),
(4, 'After Hours', 2020),
(5, 'The Inevitable End', 2014),
(6, 'Paradise Again', 2022),
(8, 'blink-182', 2003),
(7, '0', 2018),
(3, 'Drowning', 2011),
(10, 'Without you I''m nothing', 1998),
(11, 'Forever Yours', 2020);

insert into tracks(track_id, track_name, track_length, album_id)
values(1, 'Without you', 181.2, 1),
(2, 'A friend of mine', 143.4, 1),
(3, 'Special needs', 309.6, 2),
(4, 'The bitter end', 186, 2),
(5, 'In your room', 373.8, 9),
(6, 'Blinding lights', 192, 4),
(7, 'Call out my name', 201, 4),
(8, 'Monument', 267.6, 5),
(9, 'Redlight', 241.2, 6),
(10, 'Always', 246.6, 7),
(11, 'I''ll keep coming', 331.2, 8),
(12, 'English Summer Rain', 240.6, 2),
(13, 'Drowning - Avicii Remix', 194.4, 3),
(14, 'Without you I''m nothing', 244.8, 10),
(15, 'Forever Yours (Avicii Tribute)', 187.8, 11);


insert into compilations(compilation_id, compilation_name, compilation_year)
values(1, 'Headliners', 2019),
(2, 'My sweet pure melancholy', 2013),
(3, 'Top 2020', 2020),
(4, 'EDM', 2017),
(5, '00''s', 2009),
(6, 'Hideo Kojima is a genius', 2019),
(7, 'Legends', 2015),
(8, 'De nordiska musikerna', 2021);


insert into tracks_compilations (id, track_id, compilation_id)
values(1, 1, 1),
(2, 1, 4),
(3, 1, 8),
(4, 1, 7),
(5, 2, 4),
(6, 2, 8),
(7, 3, 2),
(8, 3, 5),
(9, 3, 7),
(10, 4, 2),
(11, 4, 5),
(12, 5, 2),
(13, 5, 7),
(14, 6, null),
(15, 7, 3),
(16, 8, 4),
(17, 8, 8),
(18, 9, null),
(19, 9, null),
(20, 10, 5),
(21, 11, 6),
(22, 8, 6),
(23, 12, 2),
(24, 13, 1),
(25, 13, 4),
(26, 14, 7),
(27, 14, 2),
(28, 15, 7);

update  tracks_compilations 
set compilation_id = null 
where track_id = 9;

insert into genres_artists (id, genre_id, artist_id)
values(1, 1, 1),
(2, 1, 6),
(3, 1, 9),
(4, 1, 11),
(5, 2, 2),
(6, 2, 3),
(7, 3, 5),
(8, 2, 10),
(9, 3, 8),
(10, 4, 4),
(11, 5, 7),
(12, 3, 2);

insert into artists_albums (id, artist_id, album_id)
values(1, 1, 1),
(2, 1, 11),
(3, 1, 3),
(4, 2, 10),
(5, 3, 9),
(6, 4, 4),
(7, 5, 5),
(8, 6, 6),
(9, 7, 8),
(10, 8, 7),
(11, 9, 3),
(12, 10, 10),
(13, 11, 11),
(14, 2, 2);


