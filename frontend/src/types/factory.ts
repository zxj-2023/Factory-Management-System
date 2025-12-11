export interface Part {
  part_id: string;
  name: string;
  type: string;
  unit_price: number;
  created_at?: string;
  updated_at?: string;
}

export interface Supplier {
  supplier_id: string;
  name: string;
  address?: string | null;
  phone?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface Warehouse {
  warehouse_id: string;
  address: string;
  created_at?: string;
  updated_at?: string;
}

export interface Staff {
  staff_id: string;
  name: string;
  gender?: string | null;
  hire_date: string;
  title?: string | null;
  warehouse_id: string;
  created_at?: string;
  updated_at?: string;
}

export interface Inventory {
  warehouse_id: string;
  part_id: string;
  stock_quantity: number;
  created_at?: string;
  updated_at?: string;
}

export interface Purchase {
  purchase_id: string;
  part_id: string;
  supplier_id: string;
  warehouse_id: string;
  purchase_date: string;
  quantity: number;
  actual_price: number;
  created_at?: string;
  updated_at?: string;
}
