SELECT 
    vc.*,  -- Select all columns from vietnam_casualties
    a.*    -- Select all columns from awards (this will repeat for each award)
FROM 
    vietnam_casualties vc
LEFT JOIN 
    awards a
    ON vc.last_name = a.last_name
    AND vc.first_name = a.first_name
    AND LEFT(COALESCE(vc.middle_name, ''), 1) = LEFT(COALESCE(a.middle_name, ''), 1)
    AND COALESCE(vc.suffix, '') = COALESCE(a.suffix, '')
WHERE 
    a.unique_identifier IS NOT NULL
    AND vc.member_name NOT IN (
        'MCMAHON THOMAS JOHN',
        'KING ROBERT LEE',
        'KING MONROE DEE',
        'KING ROBERT LEON',
        'KING ROBERT LEWIS',
        'KING ROBERT LOUIS',
        'HOLMES JOHN HARRIS',
        'HILL JOHN RICHARD',
        'DAVIS JOHN EDWARD',
        'DAVIS JOHN EDWIN',
        'ADAMS JAMES CLARENCE',
        'SMITH DENNIS ALLEN',
        'SMITH GARY MARTIN',
        'LONG JAMES ALLEN',
        'JONES CHARLES A',
        'DAVIS THOMAS JOEL',
        'ADAMS WILLIAM ERNEST'
    )
    -- Special case to include the one with service number
    OR (vc.member_name = 'HILL JOHN ROBERT' AND vc.service_number = '1613797')
ORDER BY 
    vc.member_name DESC;
