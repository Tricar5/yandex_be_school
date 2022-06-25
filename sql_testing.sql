
with cte as (
with cte as (select id, max(import_id) as import_id from unit_import
group by id)
select u.* from unit_import u
join cte on cte.import_id = u.import_id and cte.id = u.id;


with cte as (
with cte as (select id, max(import_id) as import_id from unit_import
group by id)
select u.* from unit_import u
join cte on cte.import_id = u.import_id and cte.id = u.id
           )
