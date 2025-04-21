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

where unique_identifier is not null