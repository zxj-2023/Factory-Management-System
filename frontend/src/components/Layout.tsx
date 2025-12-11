import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import {
  Layout as AntLayout,
  Menu,
  theme,
  Typography,
  Space,
} from 'antd';
import {
  DashboardOutlined,
  AppstoreOutlined,
  TeamOutlined,
  HomeOutlined,
  UserOutlined,
  InboxOutlined,
  ShoppingCartOutlined,
  LogoutOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { Button, message } from 'antd';
import { supabase } from '../services/supabaseClient';
import { useNavigate } from 'react-router-dom';

const { Header, Sider, Content } = AntLayout;
const { Title } = Typography;

const menuItems = [
  {
    key: '/',
    icon: <DashboardOutlined />,
    label: <Link to="/">仪表板</Link>,
  },
  {
    key: '/parts',
    icon: <AppstoreOutlined />,
    label: <Link to="/parts">零件管理</Link>,
  },
  {
    key: '/suppliers',
    icon: <TeamOutlined />,
    label: <Link to="/suppliers">供应商管理</Link>,
  },
  {
    key: '/warehouses',
    icon: <HomeOutlined />,
    label: <Link to="/warehouses">仓库管理</Link>,
  },
  {
    key: '/staff',
    icon: <UserOutlined />,
    label: <Link to="/staff">职工管理</Link>,
  },
  {
    key: '/inventory',
    icon: <InboxOutlined />,
    label: <Link to="/inventory">库存管理</Link>,
  },
  {
    key: '/purchases',
    icon: <ShoppingCartOutlined />,
    label: <Link to="/purchases">采购记录</Link>,
  },
  {
    key: '/users',
    icon: <SettingOutlined />,
    label: <Link to="/users">用户权限</Link>,
  },
];

const Layout: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      message.error('退出登录失败');
      return;
    }
    message.success('已退出登录');
    navigate('/login');
  };

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
      >
        <div style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#001529'
        }}>
          <Title
            level={4}
            style={{
              color: 'white',
              margin: 0,
              display: collapsed ? 'none' : 'block'
            }}
          >
            工厂管理系统
          </Title>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
        />
      </Sider>
      <AntLayout>
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            paddingLeft: 16,
            paddingRight: 16,
            justifyContent: 'space-between',
          }}
        >
          <Space>
            {/* 可以在这里添加面包屑导航或用户信息 */}
            <Title level={5} style={{ margin: 0 }}>
              工厂管理系统
            </Title>
          </Space>
          <Button icon={<LogoutOutlined />} onClick={handleLogout}>
            退出登录
          </Button>
        </Header>
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            minHeight: 280,
            background: colorBgContainer,
          }}
        >
          {children || <Outlet />}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
