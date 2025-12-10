-- DDL for timestamp columns and update triggers based on backend/src/db/models.py

-- Unified updated_at trigger function
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- part
ALTER TABLE part
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_part_set_updated_at ON part;
CREATE TRIGGER trg_part_set_updated_at
    BEFORE UPDATE ON part
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

-- supplier
ALTER TABLE supplier
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_supplier_set_updated_at ON supplier;
CREATE TRIGGER trg_supplier_set_updated_at
    BEFORE UPDATE ON supplier
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

-- warehouse
ALTER TABLE warehouse
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_warehouse_set_updated_at ON warehouse;
CREATE TRIGGER trg_warehouse_set_updated_at
    BEFORE UPDATE ON warehouse
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

-- staff
ALTER TABLE staff
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_staff_set_updated_at ON staff;
CREATE TRIGGER trg_staff_set_updated_at
    BEFORE UPDATE ON staff
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

-- inventory
ALTER TABLE inventory
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_inventory_set_updated_at ON inventory;
CREATE TRIGGER trg_inventory_set_updated_at
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

-- purchase
ALTER TABLE purchase
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
DROP TRIGGER IF EXISTS trg_purchase_set_updated_at ON purchase;
CREATE TRIGGER trg_purchase_set_updated_at
    BEFORE UPDATE ON purchase
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();