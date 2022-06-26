with recursive cte(
    select "parentId", avg(price)
        from unit u
    group by "parentId"
    union
    select id, price
    from unit u1
    where u1.id = u."parentId"
    )
select * from cte;

WITH RECURSIVE shop_unit(id,name,price,parent_id,type) as (
    (VALUES
        ('a','Propane',null,null,'CATEGORY'),
          ('b','Fuels',null,'a','CATEGORY'),
            ('c','HD5',5,'b','ITEM'),
            ('d','HD10',10,'b','ITEM'),
            ('e','Commercial',15,'b','ITEM'),
          ('f','Accessories',null,'a','CATEGORY'),
            ('g','Grill',100,'f','ITEM'),
            ('h','NFT',null,'f','CATEGORY'),
              ('i','bwaah.jpg',20000,'h','ITEM'),
              ('j','jaypeg.jpg',100000,'h','ITEM'),
         ('k','WD-40',2,null,'ITEM')
      )
),

unit_tree as (
    SELECT
        s1.id,
        s1.name,
        s1.price,
        s1.parent_id,
        s1.type,
        0 as level,
        array[id] as path
    FROM
      shop_unit s1
    WHERE
      s1.id = 'a'

    UNION ALL

    SELECT
      s2.id,
      s2.name,
      s2.price,
      s2.parent_id,
      s2.type,
      level + 1,
      ut.path ||  s2.id as path --generate the path for every unit so that we can check if it is a child of another element
    FROM
      shop_unit s2
      JOIN unit_tree ut ON ut.id = s2.parent_id
)

SELECT
  ut.id,
  ut.name,
  ut.parent_id,
  ut.type,
  case when ut.type = 'CATEGORY' then ap.avg_price else ut.price end as price,
  ut.level,
  ut.path

FROM
  unit_tree ut
  -- The JOIN LATERAL subquery roughly means "for each row of ut run this query"
  -- Must be a LEFT JOIN LATERAL in order to keep rows of ut that have no children.
  LEFT JOIN LATERAL (
    SELECT
      avg(ut2.price) avg_price
    FROM
      unit_tree ut2
    WHERE
      ut.level < ut2.level --is deeper level
      and  ut.id = any(path) --is in the path
    GROUP BY
      ut.id
  ) ap ON TRUE

ORDER BY id