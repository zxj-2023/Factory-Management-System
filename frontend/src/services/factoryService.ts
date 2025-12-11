import api from './api';
import { Part, Supplier, Warehouse, Staff, Inventory, Purchase } from '../types/factory';

export const getParts = async (): Promise<Part[]> => {
  const { data } = await api.get<Part[]>('/factory/parts');
  return data;
};

export const createPart = async (payload: Part) => {
  const { data } = await api.post<Part>('/factory/parts', payload);
  return data;
};

export const updatePart = async (part_id: string, payload: Partial<Part>) => {
  const { data } = await api.put<Part>(`/factory/parts/${part_id}`, payload);
  return data;
};

export const deletePart = async (part_id: string) => {
  await api.delete(`/factory/parts/${part_id}`);
};

export const getSuppliers = async (): Promise<Supplier[]> => {
  const { data } = await api.get<Supplier[]>('/factory/suppliers');
  return data;
};

export const createSupplier = async (payload: Supplier) => {
  const { data } = await api.post<Supplier>('/factory/suppliers', payload);
  return data;
};

export const updateSupplier = async (supplier_id: string, payload: Partial<Supplier>) => {
  const { data } = await api.put<Supplier>(`/factory/suppliers/${supplier_id}`, payload);
  return data;
};

export const deleteSupplier = async (supplier_id: string) => {
  await api.delete(`/factory/suppliers/${supplier_id}`);
};

export const getWarehouses = async (): Promise<Warehouse[]> => {
  const { data } = await api.get<Warehouse[]>('/factory/warehouses');
  return data;
};

export const createWarehouse = async (payload: Warehouse) => {
  const { data } = await api.post<Warehouse>('/factory/warehouses', payload);
  return data;
};

export const updateWarehouse = async (warehouse_id: string, payload: Partial<Warehouse>) => {
  const { data } = await api.put<Warehouse>(`/factory/warehouses/${warehouse_id}`, payload);
  return data;
};

export const deleteWarehouse = async (warehouse_id: string) => {
  await api.delete(`/factory/warehouses/${warehouse_id}`);
};

export const getStaff = async (): Promise<Staff[]> => {
  const { data } = await api.get<Staff[]>('/factory/staff');
  return data;
};

export const createStaff = async (payload: Staff) => {
  const { data } = await api.post<Staff>('/factory/staff', payload);
  return data;
};

export const updateStaff = async (staff_id: string, payload: Partial<Staff>) => {
  const { data } = await api.put<Staff>(`/factory/staff/${staff_id}`, payload);
  return data;
};

export const deleteStaff = async (staff_id: string) => {
  await api.delete(`/factory/staff/${staff_id}`);
};

export const getInventory = async (): Promise<Inventory[]> => {
  const { data } = await api.get<Inventory[]>('/factory/inventory');
  return data;
};

export const createInventory = async (payload: Inventory) => {
  const { data } = await api.post<Inventory>('/factory/inventory', payload);
  return data;
};

export const updateInventory = async (
  warehouse_id: string,
  part_id: string,
  payload: Partial<Inventory>
) => {
  const { data } = await api.put<Inventory>(`/factory/inventory/${warehouse_id}/${part_id}`, payload);
  return data;
};

export const deleteInventory = async (warehouse_id: string, part_id: string) => {
  await api.delete(`/factory/inventory/${warehouse_id}/${part_id}`);
};

export const getPurchases = async (): Promise<Purchase[]> => {
  const { data } = await api.get<Purchase[]>('/factory/purchases');
  return data;
};

export const createPurchase = async (payload: Purchase) => {
  const { data } = await api.post<Purchase>('/factory/purchases', payload);
  return data;
};

export const updatePurchase = async (purchase_id: string, payload: Partial<Purchase>) => {
  const { data } = await api.put<Purchase>(`/factory/purchases/${purchase_id}`, payload);
  return data;
};

export const deletePurchase = async (purchase_id: string) => {
  await api.delete(`/factory/purchases/${purchase_id}`);
};
