--название и год выхода альбомов, вышедших в 2018 году;
select album_name, album_year from albums
where album_year = 2018;

-- название и продолжительность самого длительного трека;
select track_name, track_length from tracks
order by track_length desc 
limit 1;

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

--1)количество исполнителей в каждом жанре;
select g.genre_name, count(a.artist_name)from genres g
left join genres_artists ga on g.genre_id = ga.genre_id
left join artists as a on ga.artist_id = a.artist_id
group by genre_name;

--2)количество треков, вошедших в альбомы 2019-2020 годов;
select album_year, count(track_id) from albums a
join tracks t on a.album_id = t.album_id 
where album_year between 2019 and 2020
group by album_year;

--3)средняя продолжительность треков по каждому альбому;
select album_name, avg(track_length) from albums a 
join tracks t on a.album_id = t.album_id 
group by album_name
order by avg(track_length) desc;

--4)все исполнители, которые не выпустили альбомы в 2020 году (ИСПРАВЛЕНО);
select distinct artist_name from artists as a
where a.artist_name not in (
    select distinct a.artist_name from artists a
    left join artists_albums aa on a.artist_id = aa.artist_id
    left join albums as al on al.album_id = aa.album_id
    where al.album_year = 2020
)
order by a.artist_name;

--5)названия сборников, в которых присутствует конкретный исполнитель (выберите сами) (ИСПРАВЛЕНО);
select distinct compilation_name from tracks_compilations tc 
join tracks t on tc.track_id = t.track_id 
join compilations c on tc.compilation_id = c.compilation_id 
join albums a on a.album_id = t.album_id 
join artists_albums aa on aa.album_id = a.album_id 
join artists a2 on a2.artist_id = aa.artist_id 
where artist_name like '%%Placebo%%';


--6)название альбомов, в которых присутствуют исполнители более 1 жанра;
select album_name from genres_artists ga 
join artists_albums aa on ga.artist_id = aa.artist_id 
join artists a2 on aa.artist_id = a2.artist_id 
join albums a on a.album_id = aa.album_id 
group by album_name
having count(distinct genre_id) >1;

--7)наименование треков, которые не входят в сборники (ИСПРАВЛЕНО);
select DISTINCT track_name from tracks t 
join tracks_compilations tc on tc.track_id = t.track_id 
where compilation_id is null;


--8)исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько)(ИСПРАВЛЕНО);
select a.artist_name, t.track_length from tracks as t
left join artists_albums aa on aa.album_id = t.album_id
left join artists a on a.artist_id = aa.artist_id
group by a.artist_name, t.track_length
having t.track_length = (select min(track_length) from tracks)
order by a.artist_name;


--название альбомов, содержащих наименьшее количество треков
select distinct a.album_name from albums as a
join tracks as t on t.album_id = a.album_id 
where t.album_id in (
    select album_id from tracks
    group by album_id
    having count(track_id) = (
        select count(track_id) from tracks
        group by album_id
        order by count
        limit 1
    )
)
order by a.album_name;

--название альбомов, содержащих наименьшее количество треков (ВАРИАНТ С ОДНИМ УРОВНЕМ ВЛОЖЕННОСТИ)
SELECT a.album_name, COUNT(t.track_name) Track_count FROM albums a
JOIN tracks t ON a.album_id = t.album_id 
GROUP BY a.album_name 
HAVING COUNT(t.track_name) = (
	SELECT COUNT(tracks.track_name) FROM albums
	JOIN tracks ON albums.album_id = tracks.album_id
	GROUP BY albums.album_name 
	ORDER BY COUNT(tracks.track_name)
	LIMIT 1);


