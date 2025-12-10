import { useState } from 'react';
import { Button, Card, Form, Input, message, Typography } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabaseClient';
import api from '../services/api';

const { Title } = Typography;

const Login = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values: { email: string; password: string }) => {
    setLoading(true);
    const { email, password } = values;
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    setLoading(false);
    if (error) {
      message.error(error.message || '登录失败');
      return;
    }
    // 登录成功后同步业务用户
    try {
      await api.get('/auth/sync');
    } catch (err) {
      message.warning('登录成功，但同步业务用户失败，请稍后重试');
    }
    message.success('登录成功');
    navigate('/');
  };

  return (
    <div
      style={{
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f5f5f5',
      }}
    >
      <Card style={{ width: 360 }}>
        <Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>
          工厂管理系统登录
        </Title>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="邮箱"
            name="email"
            rules={[{ required: true, message: '请输入邮箱' }, { type: 'email', message: '邮箱格式不正确' }]}
          >
            <Input placeholder="you@example.com" />
          </Form.Item>
          <Form.Item label="密码" name="password" rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password placeholder="请输入密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              登录
            </Button>
          </Form.Item>
          <div style={{ textAlign: 'right' }}>
            <Link to="/register">没有账号？去注册</Link>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Login;
