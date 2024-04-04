-- success
-- business age

SELECT businessId, MAX(rating.date)-MIN(rating.date) as businessAge
FROM rating
GROUP BY businessId;

-- average rating percentile

SELECT business.businessId, business.reviewrating-competetors.competetorrating as ratingDifference
FROM business, (SELECT business.businessId as businessId, AVG(competetor.reviewrating) as competetorrating
                FROM business as competetor, business
                WHERE (SELECT category
                    FROM BusinessCategory
                    WHERE BusinessCategory.businessId = competetor.businessId)
                    IN
                    (SELECT category
                    FROM BusinessCategory
                    WHERE BusinessCategory.businessId = business.businessId)
                GROUP BY business.businessId) competetors
WHERE business.businessId = competetors.businessId;

-- popular

-- review frequency

SELECT business.businessId as businessId, business.review_count/ages.businessAge
FROM business, (SELECT businessId, MAX(rating.date)-MIN(rating.date) as businessAge
                FROM rating
                GROUP BY businessId) ages
WHERE business.businessId = ages.businessId;

-- checkins per person

SELECT businessId, business.numCheckins/CAST(zipcodeData.population as FLOAT) as localPopularity
FROM business, zipcodeData
WHERE business.zipcode = zipcodeData.zipcode;