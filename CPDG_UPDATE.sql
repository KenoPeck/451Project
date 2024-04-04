UPDATE business set review_count = ratingTotal.count
FROM (SELECT businessId, COUNT(*) as count FROM rating GROUP BY businessId) ratingTotal
WHERE business.businessId = ratingTotal.businessId;

UPDATE business set numCheckins = checkinTotal.total
FROM (SELECT businessId, SUM(count) as total FROM checkin GROUP BY businessId) checkinTotal
WHERE business.businessId = checkinTotal.businessId;

UPDATE business set reviewrating = ratingTotal.starSum/CAST(ratingTotal.count AS decimal(7,1))
FROM (SELECT businessId, COUNT(*) as count, SUM(stars) as starSum FROM rating GROUP BY businessId) ratingTotal
WHERE business.businessId = ratingTotal.businessId;