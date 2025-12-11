import { useCallback, useEffect, useState } from 'react';
import { Card, Table, message, Button, Modal, Form, Input, Space, Popconfirm } from 'antd';
import { Purchase as PurchaseRow } from '../types/factory';
import { createPurchase, deletePurchase, getPurchases, updatePurchase } from '../services/factoryService';

const Purchases = () => {
  const [data, setData] = useState<PurchaseRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form] = Form.useForm<PurchaseRow>();
  const [editing, setEditing] = useState<PurchaseRow | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getPurchases();
      setData(res);
    } catch (err) {
      message.error('加载采购数据失败');
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

  const openEdit = (record: PurchaseRow) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      if (editing) {
        await updatePurchase(editing.purchase_id, values);
        message.success('更新成功');
      } else {
        await createPurchase(values as PurchaseRow);
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

  const handleDelete = async (record: PurchaseRow) => {
    try {
      await deletePurchase(record.purchase_id);
      message.success('删除成功');
      loadData();
    } catch {
      message.error('删除失败');
    }
  };

  return (
    <Card
      title="采购记录"
      bordered={false}
      extra={
        <Button type="primary" onClick={openCreate}>
          新增
        </Button>
      }
    >
      <Table<PurchaseRow>
        rowKey="purchase_id"
        columns={[
          { title: '单号', dataIndex: 'purchase_id' },
          { title: '零件', dataIndex: 'part_id' },
          { title: '供应商', dataIndex: 'supplier_id' },
          { title: '仓库', dataIndex: 'warehouse_id' },
          { title: '数量', dataIndex: 'quantity' },
          { title: '单价', dataIndex: 'actual_price' },
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
        title={editing ? '编辑采购' : '新增采购'}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="purchase_id"
            label="单号"
            rules={[{ required: true, message: '请输入单号' }]}
          >
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item name="part_id" label="零件" rules={[{ required: true, message: '请输入零件ID' }]}>
            <Input />
          </Form.Item>
          <Form.Item
            name="supplier_id"
            label="供应商"
            rules={[{ required: true, message: '请输入供应商ID' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="warehouse_id"
            label="仓库"
            rules={[{ required: true, message: '请输入仓库ID' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="purchase_date"
            label="采购日期"
            rules={[{ required: true, message: '请输入日期' }]}
          >
            <Input placeholder="YYYY-MM-DD" />
          </Form.Item>
          <Form.Item
            name="quantity"
            label="数量"
            rules={[{ required: true, message: '请输入数量' }]}
          >
            <Input type="number" min={1} />
          </Form.Item>
          <Form.Item
            name="actual_price"
            label="单价"
            rules={[{ required: true, message: '请输入单价' }]}
          >
            <Input type="number" min={0} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Purchases;
