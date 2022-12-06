--название и год выхода альбомов, вышедших в 2018 году;
select album_name, album_year from albums
where album_year = 2018;

-- название и продолжительность самого длительного трека;
select track_name, track_length from tracks
order by track_length desc 
limit 1;

--второй вариант:
SELECT track_name, track_length FROM tracks WHERE 
    track_length = (SELECT MAX(track_length) FROM tracks);

-- название треков, продолжительность которых не менее 3,5 минуты;
select track_name from tracks
where track_length >= 210;

-- названия сборников, вышедших в период с 2018 по 2020 год включительно;
select compilation_name from compilations
where compilation_year between 2018 and 2020;

-- исполнители, чье имя состоит из 1 слова;
select artist_name from artists
where artist_name not like '%% %%';

--название треков, которые содержат слово "мой"/"my".
select track_name from tracks where track_name like '%my%' or track_name like '%мой%';
