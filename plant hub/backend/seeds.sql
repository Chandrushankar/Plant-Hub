USE plant_hub;

-- Disable Key Checks to avoid FK errors during reload
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE plant_care;
TRUNCATE TABLE plants;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Insert Plants
INSERT INTO plants (id, plant_name, scientific_name, price, category, difficulty_level, image_url, stock_quantity) VALUES 
(1, 'Snake Plant', 'Sansevieria trifasciata', 25.00, 'indoor', 'easy', 'https://i.imgur.com/kS9w0wW.png', 50),
(2, 'Peace Lily', 'Spathiphyllum', 30.00, 'indoor', 'medium', 'https://i.imgur.com/6J7x8yZ.png', 30),
(3, 'Aloe Vera', 'Aloe barbadensis miller', 18.00, 'indoor', 'easy', 'https://i.imgur.com/1C0w0wW.png', 40);

-- 2. Insert Care Guides (Linked to Plant IDs)
INSERT INTO plant_care (plant_id, soil_type, watering_schedule, sunlight_requirement, fertilizer_info, common_problems, care_tips) VALUES 
(1, 'Sandy, well-draining soil', 'Every 2-3 weeks', 'Low to Bright indirect light', 'Diluted cactus fertilizer in summer', 'Root rot if overwatered', 'Wipe leaves to keep pores open.'),
(2, 'Rich potting mix', 'Weekly (keep soil moist)', 'Partial shade', 'Balanced houseplant fertilizer', 'Brown tips from dry air', 'Mist leaves frequently.'),
(3, 'Cactus/Succulent mix', 'Every 3 weeks (let dry completely)', 'Bright, direct sunlight', 'Succulent food in spring', 'Soft leaves from overwatering', 'Harvest lower leaves for gel.');

SELECT "Seeds imported successfully!" as result;
