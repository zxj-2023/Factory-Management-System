import { useCallback, useEffect, useState } from 'react';
import { Card, Table, message, Button, Modal, Form, Input, Space, Popconfirm } from 'antd';
import { Supplier } from '../types/factory';
import { createSupplier, deleteSupplier, getSuppliers, updateSupplier } from '../services/factoryService';

const Suppliers = () => {
  const [data, setData] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form] = Form.useForm<Supplier>();
  const [editing, setEditing] = useState<Supplier | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getSuppliers();
      setData(res);
    } catch (err) {
      message.error('加载供应商数据失败');
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

  const openEdit = (record: Supplier) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      if (editing) {
        await updateSupplier(editing.supplier_id, values);
        message.success('更新成功');
      } else {
        await createSupplier(values);
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

  const handleDelete = async (record: Supplier) => {
    try {
      await deleteSupplier(record.supplier_id);
      message.success('删除成功');
      loadData();
    } catch {
      message.error('删除失败');
    }
  };

  return (
    <Card
      title="供应商管理"
      bordered={false}
      extra={
        <Button type="primary" onClick={openCreate}>
          新增
        </Button>
      }
    >
      <Table<Supplier>
        rowKey="supplier_id"
        columns={[
          { title: '编号', dataIndex: 'supplier_id' },
          { title: '名称', dataIndex: 'name' },
          { title: '地址', dataIndex: 'address' },
          { title: '电话', dataIndex: 'phone' },
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
        title={editing ? '编辑供应商' : '新增供应商'}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="supplier_id"
            label="编号"
            rules={[{ required: true, message: '请输入编号' }]}
          >
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入名称' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item name="address" label="地址">
            <Input />
          </Form.Item>
          <Form.Item name="phone" label="电话">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Suppliers;
