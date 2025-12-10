import { Card, Row, Col, Statistic } from 'antd';
import {
  AppstoreOutlined,
  TeamOutlined,
  HomeOutlined,
  UserOutlined,
  InboxOutlined,
  ShoppingCartOutlined
} from '@ant-design/icons';

const Dashboard = () => {
  // TODO: 从 API 获取实际数据
  const stats = [
    {
      title: '零件总数',
      value: 150,
      prefix: <AppstoreOutlined />,
      color: '#1890ff',
    },
    {
      title: '供应商数量',
      value: 25,
      prefix: <TeamOutlined />,
      color: '#52c41a',
    },
    {
      title: '仓库数量',
      value: 5,
      prefix: <HomeOutlined />,
      color: '#722ed1',
    },
    {
      title: '职工人数',
      value: 80,
      prefix: <UserOutlined />,
      color: '#eb2f96',
    },
  ];

  return (
    <div>
      <h2>仪表板</h2>
      <Row gutter={16}>
        {stats.map((stat, index) => (
          <Col span={6} key={index}>
            <Card>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={stat.prefix}
                valueStyle={{ color: stat.color }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="库存预警" bordered={false}>
            <p>暂无库存预警信息</p>
            {/* TODO: 实现库存预警列表 */}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="最近采购" bordered={false}>
            <p>暂无最近采购记录</p>
            {/* TODO: 实现最近采购列表 */}
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;