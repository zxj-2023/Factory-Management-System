import api from './api';
import { AppUser, UserRole } from '../types/user';

export interface UserQuery {
  email?: string;
  role?: UserRole;
  warehouse_id?: string;
}

export interface UpdateUserPayload {
  display_name?: string | null;
  role?: UserRole;
  warehouse_id?: string | null;
}

export const fetchUsers = async (params: UserQuery = {}) => {
  const { data } = await api.get<AppUser[]>('/users', { params });
  return data;
};

export const updateUser = async (id: string, payload: UpdateUserPayload) => {
  const { data } = await api.put<AppUser>(`/users/${id}`, payload);
  return data;
};
