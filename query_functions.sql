--Actor (actor_id INT PRIMARY KEY, actor_name VARCHAR(100));
--Director (director_id INT PRIMARY KEY, director_name VARCHAR(100));
--Stars (actor_id INT, movie_id INT, PRIMARY KEY (actor_id, movie_id)); --have multiple actors
--Genre (genre VARCHAR(20), movie_id INT, PRIMARY KEY (genre, movie_id)); --have multiple genres
--Movie (movie_id INT PRIMARY KEY, movie_title VARCHAR(50), director_id INT, metacritic INT, imdb_rate NUMERIC (3,1), gross BIGINT, budget BIGINT);

-- Returns list of remaining actor names that are still hirable 
CREATE FUNCTION remaining_actors (budget BIGINT) 
	RETURNS TABLE (names VARCHAR(100)) as $$
	BEGIN
		return query select distinct a.actor_name
		from actor as a
		where cost_of_hire(a.actor_id, 0) <= budget
		order by a.actor_name asc;
	END; $$ 
LANGUAGE plpgsql;

-- Returns list of remaining director names that are still hirable 
CREATE FUNCTION remaining_directors (budget BIGINT) 
	RETURNS TABLE (names VARCHAR(100)) as $$
	BEGIN
		return query select distinct d.director_name
		from director as d
		where cost_of_hire(d.director_id, 1) <= budget
		order by d.director_name asc;
	END; $$ 
LANGUAGE plpgsql;

-- Returns list of hirable actor_id and sample movie title matching actor name
CREATE FUNCTION match_name_actor (rem_budget BIGINT, match_name VARCHAR(100)) 
	RETURNS TABLE (actor_id int, movie_name VARCHAR(50)) as $$
	BEGIN
		return query select distinct on (a.actor_id) a.actor_id, m.movie_title
		from actor as a, movie as m, stars as s
		where s.actor_id = a.actor_id and s.movie_id = m.movie_id and a.actor_name LIKE match_name and cost_of_hire(a.actor_id, 0) <= rem_budget;
	END; $$ 
LANGUAGE plpgsql;

-- Returns list of hirable director_id and sample movie title matching director name
CREATE FUNCTION match_name_director (rem_budget BIGINT, match_name VARCHAR(100)) 
	RETURNS TABLE (director_id int, movie_name VARCHAR(50)) as $$
	BEGIN
		return query select distinct on (d.director_id) d.director_id, m.movie_title
		from director as d, movie as m
		where d.director_name LIKE match_name and cost_of_hire(d.director_id, 1) <= rem_budget and m.director_id = d.director_id;
	END; $$ 
LANGUAGE plpgsql;

-- Returns list of genres in databasse
CREATE FUNCTION list_genres () 
	RETURNS TABLE (genres VARCHAR(20)) as $$
	BEGIN
		return query select distinct g.genre
		from genre as g
		order by g.genre asc;
	END; $$ 
LANGUAGE plpgsql;

-- Determines budget based on genre (as average of the budget of all movies in database of that genre)
CREATE FUNCTION make_budget (picked_genre VARCHAR(20), out new_budget BIGINT)
	RETURNS BIGINT as $$
	BEGIN
		select avg(m.budget) into new_budget
		from movie as m, genre as g
		where g.movie_id = m.movie_id and g.genre LIKE picked_genre;
	END; $$ 
LANGUAGE plpgsql;	

-- Determines cost of hiring an individual as 1/4 of budget of all movies where they appear in that role
CREATE FUNCTION cost_of_hire (id INT, dir INT, out cost BIGINT) --0 if actor, 1 if director
	RETURNS BIGINT as $$
	BEGIN
		select avg(m.budget) / 4 into cost
		from movie as m, stars as s
		where (dir = 0 and s.movie_id = m.movie_id and id = s.actor_id) or
		      (dir = 1 and id = m.director_id);
	END; $$ 
LANGUAGE plpgsql;

CREATE FUNCTION rating_generated_m (id INT, dir INT, out rating int)
	--metacritic rating contribution: 40% for director and 20% for actors
	--dir: 0 if actor, 1 if director
	RETURNS int as $$
	BEGIN
		select avg(m.metacritic) * (dir + 1) / 5 into rating
		from movie as m, stars as s
		where (dir = 0 and s.movie_id = m.movie_id and id = s.actor_id) or
		      (dir = 1 and id = m.director_id);
	END; $$ 
LANGUAGE plpgsql;

CREATE FUNCTION rating_generated_i (id INT, dir INT, out rating numeric(3, 1))
	--imdb rating contribution: 40% for director and 20% for actors
	--dir: 0 if actor, 1 if director
	RETURNS numeric(3,1) as $$
	BEGIN
		select avg(m.imdb_rate) * (dir + 1) / 5 into rating
		from movie as m, stars as s
		where (dir = 0 and s.movie_id = m.movie_id and id = s.actor_id) or
		      (dir = 1 and id = m.director_id);
	END; $$ 
LANGUAGE plpgsql;

-- Determines revenue generated by an individual as 1/4 of average revenue from all movies where they appear in that role
CREATE FUNCTION revenue (id INT, dir INT, out makes BIGINT) --0 if actor, 1 if director
	RETURNS BIGINT as $$
	BEGIN
		select avg(m.gross) / 4 into makes
		from movie as m, stars as s
		where (dir = 0 and s.movie_id = m.movie_id and id = s.actor_id) or
		      (dir = 1 and id = m.director_id);
	END; $$ 
LANGUAGE plpgsql;
