// 零件类型
export interface Part {
  part_id: string;
  name: string;
  unit_price: number;
  type: string;
}

// 供应商类型
export interface Supplier {
  supplier_id: string;
  name: string;
  address?: string;
  phone?: string;
}

// 仓库类型
export interface Warehouse {
  warehouse_id: string;
  address: string;
}

// 职工类型
export interface Staff {
  staff_id: string;
  name: string;
  gender: 'M' | 'F';
  hire_date: string;
  title?: string;
  warehouse_id: string;
}

// 库存类型
export interface Inventory {
  warehouse_id: string;
  part_id: string;
  stock_quantity: number;
}

// 采购记录类型
export interface Purchase {
  purchase_id: string;
  part_id: string;
  supplier_id: string;
  warehouse_id: string;
  purchase_date: string;
  quantity: number;
  actual_price: number;
}

// API 响应类型
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

// 分页类型
export interface PaginationParams {
  page?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}