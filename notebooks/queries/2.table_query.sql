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
 primary key(prdKind)
);

CREATE TABLE RawMtrls
(
 rawMtrl TEXT, 
 superRawMtrl TEXT,
 primary key(rawMtrl)
);

CREATE TABLE AllergyPrdKinds
(
 allergy_kind TEXT,
 superPrdKind TEXT,
 isCrossReact TEXT,
 ParentAllergy TEXT,
 probablility TEXT,
 primary key(allergy_kind)

);

CREATE TABLE VegRestrictPrdKind
(
 veg_kind TEXT,
 superPrdKind TEXT,
 primary key(veg_kind)
);

CREATE TABLE AllergyRawMtrls
(
 allergy_kind TEXT,
 superRawMtrl TEXT,
 isCrossReact TEXT,
 ParentAllergy TEXT,
 probablility TEXT,
 primary key(allergy_kind)

);

CREATE TABLE VegRestrictRawMtrls
(
 veg_kind TEXT,
 superRawMtrl TEXT,
 primary key(veg_kind)
);

CREATE TABLE UserTable (
 userID TEXT,
 name TEXT,
 gender gen,
 age INT,
 allergy allergy[],
 vName veg,
 primary key(userID)
);

CREATE TABLE DietManage (
 userID TEXT,
 date DATE NOT NULL DEFAULT CURRENT_DATE,
 eatenFood VARCHAR(255)[],
 primary key(userID, date)
);