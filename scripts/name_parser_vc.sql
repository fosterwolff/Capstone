SELECT 
    member_name, 
    LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1 AS word_count,
    CASE 
        WHEN RIGHT(member_name, 3) = ' JR' THEN 'Yes' 
        ELSE 'No' 
    END AS ends_with_JR,
    CASE 
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) = ' JR' THEN 'True'
        ELSE 'False'
    END AS no_middle_name,
    CASE
        -- Parsing for word_count = 4 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 4
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 1)  -- Last name
        -- Parsing for word_count = 3 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 1)  -- Last name
        -- Parsing for word_count = 3 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) != ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 1)  -- Last name
        -- Parsing for word_count = 2 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 2
             AND RIGHT(member_name, 3) != ' JR' THEN
                 SPLIT_PART(member_name, ' ', 1)  -- Last name
        ELSE NULL
    END AS last_name,
    CASE
        -- Parsing for word_count = 4 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 4
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 2)  -- First name
        -- Parsing for word_count = 3 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) = ' JR' THEN
                 SPLIT_PART(member_name, ' ', 2)  -- First name
        -- Parsing for word_count = 3 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) != ' JR' THEN
                 SPLIT_PART(member_name, ' ', 2)  -- First name
        -- Parsing for word_count = 2 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 2
             AND RIGHT(member_name, 3) != ' JR' THEN
                 SPLIT_PART(member_name, ' ', 2)  -- First name
        ELSE NULL
    END AS first_name,
    CASE
        -- Parsing for word_count = 4 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 4
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 3)  -- Middle name
        -- Parsing for word_count = 3 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 NULL  -- Middle name will be NULL for 3-word name ending with JR
        -- Parsing for word_count = 3 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) != ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 3)  -- Middle name
        -- Parsing for word_count = 2 and does not end with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 2
             AND RIGHT(member_name, 3) != ' JR' THEN 
                 NULL  -- Middle name will be NULL for 2-word name
        ELSE NULL
    END AS middle_name,
    CASE
        -- Parsing for word_count = 4 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 4
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 4)  -- Suffix (JR)
        -- Parsing for word_count = 3 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 3
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 SPLIT_PART(member_name, ' ', 3)  -- Suffix (JR) for 3-word name
        -- Parsing for word_count = 2 and ends with JR
        WHEN (LENGTH(member_name) - LENGTH(REPLACE(member_name, ' ', '')) + 1) = 2
             AND RIGHT(member_name, 3) = ' JR' THEN 
                 NULL  -- Suffix is NULL for 2-word name ending with JR
        ELSE NULL
    END AS suffix
FROM vietnam_casualties;
