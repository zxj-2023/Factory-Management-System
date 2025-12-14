import { useCallback, useEffect, useMemo, useState } from 'react';
import { Card, Table, message, Button, Modal, Form, Input, Space, Popconfirm, Select } from 'antd';
import { Inventory as InventoryRow } from '../types/factory';
import {
  createInventory,
  deleteInventory,
  getInventory,
  updateInventory,
  getParts,
  getWarehouses,
} from '../services/factoryService';

const Inventory = () => {
  const [data, setData] = useState<InventoryRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form] = Form.useForm<InventoryRow>();
  const [editing, setEditing] = useState<InventoryRow | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [partOptions, setPartOptions] = useState<{ label: string; value: string }[]>([]);
  const [warehouseOptions, setWarehouseOptions] = useState<{ label: string; value: string }[]>([]);
  const partLabelMap = useMemo(
    () => Object.fromEntries(partOptions.map((p) => [p.value, p.label])),
    [partOptions]
  );
  const warehouseLabelMap = useMemo(
    () => Object.fromEntries(warehouseOptions.map((w) => [w.value, w.label])),
    [warehouseOptions]
  );

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getInventory();
      setData(res);
    } catch (err) {
      message.error('加载库存数据失败');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadFKOptions = useCallback(async () => {
    try {
      const [parts, warehouses] = await Promise.all([getParts(), getWarehouses()]);
      setPartOptions(parts.map((p) => ({ label: `${p.part_id} - ${p.name}`, value: p.part_id })));
      setWarehouseOptions(
        warehouses.map((w) => ({
          label: `${w.warehouse_id} - ${w.address ?? ''}`,
          value: w.warehouse_id,
        }))
      );
    } catch {
      message.error('加载关联选项失败，请刷新后重试');
    }
  }, []);

  useEffect(() => {
    loadData();
    loadFKOptions();
  }, [loadData, loadFKOptions]);

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    setModalOpen(true);
  };

  const openEdit = (record: InventoryRow) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      if (editing) {
        await updateInventory(editing.warehouse_id, editing.part_id, values);
        message.success('更新成功');
      } else {
        await createInventory(values);
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

  const handleDelete = async (record: InventoryRow) => {
    try {
      await deleteInventory(record.warehouse_id, record.part_id);
      message.success('删除成功');
      loadData();
    } catch {
      message.error('删除失败');
    }
  };

  return (
    <Card
      title="库存管理"
      bordered={false}
      extra={
        <Button type="primary" onClick={openCreate}>
          新增
        </Button>
      }
    >
      <Table<InventoryRow>
        rowKey={(row) => `${row.warehouse_id}-${row.part_id}`}
        columns={[
          {
            title: '仓库',
            dataIndex: 'warehouse_id',
            render: (v: string) => warehouseLabelMap[v] || v,
          },
          {
            title: '零件',
            dataIndex: 'part_id',
            render: (v: string) => partLabelMap[v] || v,
          },
          { title: '库存数量', dataIndex: 'stock_quantity' },
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
        title={editing ? '编辑库存' : '新增库存'}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="warehouse_id"
            label="仓库"
            rules={[{ required: true, message: '请选择仓库' }]}
          >
            <Select
              placeholder="选择仓库"
              options={warehouseOptions}
              showSearch
              optionFilterProp="label"
              disabled={!!editing}
            />
          </Form.Item>
          <Form.Item
            name="part_id"
            label="零件"
            rules={[{ required: true, message: '请选择零件' }]}
          >
            <Select
              placeholder="选择零件"
              options={partOptions}
              showSearch
              optionFilterProp="label"
              disabled={!!editing}
            />
          </Form.Item>
          <Form.Item
            name="stock_quantity"
            label="库存数量"
            rules={[{ required: true, message: '请输入库存数量' }]}
          >
            <Input type="number" min={0} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Inventory;
