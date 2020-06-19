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

CREATE TABLE PrdKinds
(
 prdKind TEXT,
 superPrdKind TEXT,
 isCrossReact BOOLEAN,
 ParentAllergy TEXT[],
 probability numeric(2,1),
 primary key(prdKind)
);

CREATE TABLE RawMtrls
(
 rawMtrl TEXT, 
 superRawMtrl TEXT,
 isCrossReact BOOLEAN,
 ParentAllergy TEXT[],
 probability numeric(2,1),
 primary key(rawMtrl)
);

CREATE TABLE AllergyPrdKinds
(
 allergy_kind allergy,
 superPrdKind TEXT[],
 primary key(allergy_kind)
);

CREATE TABLE VegRestrictPrdKind
(
 veg_kind veg,
 superPrdKind TEXT,
 primary key(veg_kind)
);

CREATE TABLE AllergyRawMtrls
(
 allergy_kind allergy,
 superRawMtrl TEXT,
 primary key(allergy_kind)

);

CREATE TABLE VegRestrictRawMtrls
(
 veg_kind veg,
 RawMtrl TEXT,
 primary key(veg_kind)
);
