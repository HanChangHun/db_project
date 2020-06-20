create or replace function f1() returns trigger as $AllergyTrigger$
    begin
        insert into AllergyProduct select New.prdlstreportno, r.*
        from allergyrawmtrl r
        where New.rawMtrl LIKE '%%' || r.rawmtrl || '%%';
        return null;
    end;
$AllergyTrigger$ language plpgsql;

create trigger AllergyTrigger
after insert on FoodInfo
for each row
execute procedure f1();

create or replace function f2() returns trigger as $VegTrigger$
    begin
        insert into VegProduct select New.prdlstreportno, r.*
        from vegrawmtrl r
        where New.rawMtrl LIKE '%%' || r.rawmtrl || '%%';
        return null;
    end;
$VegTrigger$ language plpgsql;

create trigger VegTrigger
after insert on FoodInfo
for each row
execute procedure f2();

