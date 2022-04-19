select hex7
  from (select 0 as color_id, '#FF6666' as hex7, '#FF0000' as hex5, '#CC0000' as hex4 union
        select 1, '#FFB266', '#FF8000', '#CC6600' union
        select 2, '#FFFF66', '#FFFF00', '#CCCC00' union
        select 3, '#B2FF66', '#80FF00', '#66CC00' union
        select 4, '#66FF66', '#00FF00', '#00CC00' union
        select 5, '#66FFB2', '#00FF80', '#00CC66' union
        select 6, '#66FFFF', '', '#00CCCC' union
        select 7, '#66B2FF', '', '#0066CC' union
        select 8, '#6666FF', '', '#0000CC' union
        select 9, '#B266FF', '', '#00CC66' union
        select 10, '#FF66FF', '', '#6600CC' union
        select 11, '#FF66B2', '', '#CC00CC' union
        select 12, '#C0C0C0', '', '#CC0066') as clrs
 where clrs.color_id = mod(id, 11)
