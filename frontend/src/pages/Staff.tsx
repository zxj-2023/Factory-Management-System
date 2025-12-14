import { useCallback, useEffect, useMemo, useState } from 'react';
import { Card, Table, message, Button, Modal, Form, Input, Space, Popconfirm, Select } from 'antd';
import { Staff as StaffRow } from '../types/factory';
import { createStaff, deleteStaff, getStaff, updateStaff, getWarehouses } from '../services/factoryService';

const Staff = () => {
  const [data, setData] = useState<StaffRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form] = Form.useForm<StaffRow>();
  const [editing, setEditing] = useState<StaffRow | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [warehouseOptions, setWarehouseOptions] = useState<{ label: string; value: string }[]>([]);
  const warehouseLabelMap = useMemo(
    () => Object.fromEntries(warehouseOptions.map((w) => [w.value, w.label])),
    [warehouseOptions]
  );

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getStaff();
      setData(res);
    } catch (err) {
      message.error('加载职工数据失败');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadFKOptions = useCallback(async () => {
    try {
      const warehouses = await getWarehouses();
      setWarehouseOptions(
        warehouses.map((w) => ({
          label: `${w.warehouse_id} - ${w.address ?? ''}`,
          value: w.warehouse_id,
        }))
      );
    } catch {
      message.error('加载仓库选项失败');
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

  const openEdit = (record: StaffRow) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      if (editing) {
        const { name, gender, hire_date, title, warehouse_id } = values;
        await updateStaff(editing.staff_id, { name, gender, hire_date, title, warehouse_id });
        message.success('更新成功');
      } else {
        await createStaff(values as StaffRow);
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

  const handleDelete = async (record: StaffRow) => {
    try {
      await deleteStaff(record.staff_id);
      message.success('删除成功');
      loadData();
    } catch {
      message.error('删除失败');
    }
  };

  return (
    <Card
      title="职工管理"
      bordered={false}
      extra={
        <Button type="primary" onClick={openCreate}>
          新增
        </Button>
      }
    >
      <Table<StaffRow>
        rowKey="staff_id"
        columns={[
          { title: '编号', dataIndex: 'staff_id' },
          { title: '姓名', dataIndex: 'name' },
          { title: '职称', dataIndex: 'title' },
          {
            title: '仓库',
            dataIndex: 'warehouse_id',
            render: (v: string | null) => (v ? warehouseLabelMap[v] || v : ''),
          },
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
        title={editing ? '编辑职工' : '新增职工'}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="staff_id"
            label="编号"
            rules={[{ required: true, message: '请输入编号' }]}
          >
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item name="name" label="姓名" rules={[{ required: true, message: '请输入姓名' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="gender" label="性别">
            <Select allowClear options={[{ label: 'M', value: 'M' }, { label: 'F', value: 'F' }]} />
          </Form.Item>
          <Form.Item
            name="hire_date"
            label="入职日期"
            rules={[{ required: true, message: '请输入入职日期' }]}
          >
            <Input placeholder="YYYY-MM-DD" />
          </Form.Item>
          <Form.Item name="title" label="职称">
            <Input />
          </Form.Item>
          <Form.Item
            name="warehouse_id"
            label="仓库"
            rules={[{ required: true, message: '请选择仓库' }]}
          >
            <Select
              allowClear
              placeholder="选择仓库（可空）"
              options={warehouseOptions}
              showSearch
              optionFilterProp="label"
            />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Staff;
