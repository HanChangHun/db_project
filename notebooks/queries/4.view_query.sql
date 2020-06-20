create view VegProduct as select prdlstReportNo, P.*
from FoodInfo F, VegPrdKind P
where F.prdKind = P.prdKind;

create view AllergyProduct as select prdlstReportNo, P.*
from FoodInfo F, AllergyPrdKind P
where F.prdKind = P.prdKind;

