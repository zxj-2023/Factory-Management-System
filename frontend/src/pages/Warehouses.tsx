import { useCallback, useEffect, useState } from 'react';
import { Card, Table, message, Button, Modal, Form, Input, Space, Popconfirm } from 'antd';
import { Warehouse } from '../types/factory';
import { createWarehouse, deleteWarehouse, getWarehouses, updateWarehouse } from '../services/factoryService';

const Warehouses = () => {
  const [data, setData] = useState<Warehouse[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form] = Form.useForm<Warehouse>();
  const [editing, setEditing] = useState<Warehouse | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getWarehouses();
      setData(res);
    } catch (err) {
      message.error('加载仓库数据失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    setModalOpen(true);
  };

  const openEdit = (record: Warehouse) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      if (editing) {
        await updateWarehouse(editing.warehouse_id, values);
        message.success('更新成功');
      } else {
        await createWarehouse(values);
        message.success('创建成功');
      }
      setModalOpen(false);
      loadData();
    } catch (err) {
      message.error('保存失败');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (record: Warehouse) => {
    try {
      await deleteWarehouse(record.warehouse_id);
      message.success('删除成功');
      loadData();
    } catch {
      message.error('删除失败');
    }
  };

  return (
    <Card
      title="仓库管理"
      bordered={false}
      extra={
        <Button type="primary" onClick={openCreate}>
          新增
        </Button>
      }
    >
      <Table<Warehouse>
        rowKey="warehouse_id"
        columns={[
          { title: '编号', dataIndex: 'warehouse_id' },
          { title: '地址', dataIndex: 'address' },
          {
            title: '操作',
            render: (_, record) => (
              <Space>
                <Button type="link" onClick={() => openEdit(record)}>
                  编辑
                </Button>
                <Popconfirm title="确认删除？" onConfirm={() => handleDelete(record)}>
                  <Button type="link" danger>
                    删除
                  </Button>
                </Popconfirm>
              </Space>
            ),
          },
        ]}
        dataSource={data}
        loading={loading}
        pagination={false}
      />

      <Modal
        title={editing ? '编辑仓库' : '新增仓库'}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="warehouse_id"
            label="编号"
            rules={[{ required: true, message: '请输入编号' }]}
          >
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item
            name="address"
            label="地址"
            rules={[{ required: true, message: '请输入地址' }]}
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Warehouses;
