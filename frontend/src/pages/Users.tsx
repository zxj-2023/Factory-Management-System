import { useEffect, useState } from 'react';
import { Button, Form, Input, Modal, Select, Space, Table, message, Card } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { fetchUsers, updateUser } from '../services/userService';
import { AppUser, UserRole } from '../types/user';

const roleOptions = [
  { label: '管理员', value: 'admin' },
  { label: '仓库主管', value: 'warehouse_manager' },
  { label: '采购员', value: 'purchaser' },
  { label: '库存操作员', value: 'inventory_operator' },
];

const Users = () => {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState<AppUser[]>([]);
  const [queryForm] = Form.useForm();
  const [editForm] = Form.useForm();
  const [editingUser, setEditingUser] = useState<AppUser | null>(null);
  const [saving, setSaving] = useState(false);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const params = queryForm.getFieldsValue();
      const data = await fetchUsers(params);
      setUsers(data);
    } catch (err) {
      message.error('获取用户列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleSearch = () => {
    loadUsers();
  };

  const handleReset = () => {
    queryForm.resetFields();
    loadUsers();
  };

  const openEdit = (record: AppUser) => {
    setEditingUser(record);
    editForm.setFieldsValue({
      display_name: record.display_name,
      role: record.role,
      warehouse_id: record.warehouse_id,
    });
  };

  const handleUpdate = async () => {
    if (!editingUser) return;
    try {
      setSaving(true);
      const values = await editForm.validateFields();
      await updateUser(editingUser.id, values);
      message.success('更新成功');
      setEditingUser(null);
      loadUsers();
    } catch (err) {
      message.error('更新失败');
    } finally {
      setSaving(false);
    }
  };

  const columns: ColumnsType<AppUser> = [
    { title: '邮箱', dataIndex: 'email', key: 'email' },
    { title: '显示名', dataIndex: 'display_name', key: 'display_name' },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (value: UserRole) => {
        const opt = roleOptions.find((o) => o.value === value);
        return opt?.label || value;
      },
    },
    { title: '仓库', dataIndex: 'warehouse_id', key: 'warehouse_id' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Button type="link" onClick={() => openEdit(record)}>
          编辑
        </Button>
      ),
    },
  ];

  return (
    <Card title="用户权限管理">
      <Form form={queryForm} layout="inline" style={{ marginBottom: 16 }}>
        <Form.Item name="email" label="邮箱">
          <Input allowClear placeholder="输入邮箱关键词" />
        </Form.Item>
        <Form.Item name="role" label="角色">
          <Select allowClear style={{ width: 180 }} options={roleOptions} />
        </Form.Item>
        <Form.Item name="warehouse_id" label="仓库">
          <Input allowClear placeholder="仓库ID" />
        </Form.Item>
        <Form.Item>
          <Space>
            <Button type="primary" onClick={handleSearch}>
              查询
            </Button>
            <Button onClick={handleReset}>重置</Button>
          </Space>
        </Form.Item>
      </Form>

      <Table<AppUser> rowKey="id" loading={loading} columns={columns} dataSource={users} />

      <Modal
        title="编辑用户"
        open={!!editingUser}
        onCancel={() => setEditingUser(null)}
        onOk={handleUpdate}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={editForm} layout="vertical">
          <Form.Item label="邮箱">
            <Input value={editingUser?.email} disabled />
          </Form.Item>
          <Form.Item name="display_name" label="显示名">
            <Input placeholder="输入显示名" />
          </Form.Item>
          <Form.Item
            name="role"
            label="角色"
            rules={[{ required: true, message: '请选择角色' }]}
          >
            <Select options={roleOptions} />
          </Form.Item>
          <Form.Item name="warehouse_id" label="仓库">
            <Input placeholder="仓库ID" />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Users;
