CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT parents.child from parents,dogs where dogs.name = parents.parent ORDER BY dogs.height DESC;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT dogs.name,sizes.size from dogs,sizes where sizes.min < dogs.height 
  and dogs.height <= sizes.max order by dogs.height desc;


-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child as first1 ,b.child as second2
  from parents as a,parents as b
  where a.parent = b.parent and a.child < b.child;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT  "The two siblings, " || first1|| " and " || second2 || ", have the same size: "|| a.size 
  from siblings,size_of_dogs as a, size_of_dogs as b
  where a.size = b.size and a.name = first1 and b.name = second2;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT fur ,max(height) - min(height) as height_range from dogs group by fur
  having max(height) <= AVG(height) * 1.3 and min(height) >= AVG(height) * 0.7;

