CREATE TABLE FoodInfo
(
 prdlstReportNo TEXT,
 prdlstName TEXT,
 rawMtrl TEXT,
 allergy TEXT,
 nutrient TEXT,
 barcode TEXT,
 prdKind TEXT,
 manufacture TEXT,
 seller TEXT,
 capacity TEXT,
 imgurl1 TEXT,
 imgurl2 TEXT,
 primary key(prdlstReportNo)
);

CREATE TABLE AllergyPrdKind
(
 prdKind TEXT,
 allergy allergy,
 isCrossReact BOOLEAN,
 probablility numeric(2,1),
 primary key(prdKind)
);

CREATE TABLE AllergyRawMtrl
(
 rawMtrl TEXT,
 allergy allergy,
 isCrossReact BOOLEAN,
 probablility numeric(2,1),
 primary key(rawMtrl)
);

CREATE TABLE VegPrdKind
(
 prdKind TEXT,
 vegan BOOLEAN,
 lactoVeg BOOLEAN,
 ovoVeg BOOLEAN,
 lactoOvoVeg BOOLEAN,
 pescoVeg BOOLEAN,
 polloVeg BOOLEAN,
 primary key(prdKind)
);

CREATE TABLE VegRawMtrl
(
 rawMtrl TEXT,
 vegan BOOLEAN,
 lactoVeg BOOLEAN,
 ovoVeg BOOLEAN,
 lactoOvoVeg BOOLEAN,
 pescoVeg BOOLEAN,
 polloVeg BOOLEAN,
 primary key(rawMtrl)
);

CREATE TABLE IF NOT EXISTS UserTable (
 userID TEXT,
 password TEXT,
 gender gen,
 age INT,
 allergies allergy[],
 vName veg,
 primary key(userID)
);