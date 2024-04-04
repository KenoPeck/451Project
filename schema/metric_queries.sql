-- success
-- business age

SELECT businessId, EXTRACT(days from MAX(rating.date)-MIN(rating.date)) as businessAge
FROM rating
GROUP BY businessId
ORDER BY businessAge;

-- average rating difference

SELECT business.businessId as businessId, business.reviewrating - AVG(competetor.reviewrating) as ratingDifference
FROM business as competetor, business
WHERE business.businessId <> competetor.businessId and
    EXISTS (SELECT category 
            FROM BusinessCategory
            WHERE BusinessCategory.businessId = business.businessId and
                category IN (SELECT category 
                        FROM BusinessCategory
                        WHERE BusinessCategory.businessId = competetor.businessId))
GROUP BY business.businessId
ORDER BY ratingDifference;

-- popular

-- review frequency

SELECT business.businessId as businessId, business.review_count/ages.businessAge as reviewFrequency
FROM business, (SELECT businessId, EXTRACT(days from MAX(rating.date)-MIN(rating.date)) as businessAge
                FROM rating
                GROUP BY businessId) ages
WHERE business.businessId = ages.businessId and ages.businessAge <> 0
ORDER BY reviewFrequency;

-- checkins per person

SELECT businessId, business.numCheckins/CAST(zipcodeData.population as FLOAT) as localPopularity
FROM business, zipcodeData
WHERE business.zipcode = zipcodeData.zipcode
ORDER BY localPopularity;