export type UserRole = 'admin' | 'warehouse_manager' | 'purchaser' | 'inventory_operator';

export interface AppUser {
  id: string;
  auth_user_id: string;
  email: string;
  display_name?: string | null;
  role: UserRole;
  warehouse_id?: string | null;
  created_at?: string;
}
