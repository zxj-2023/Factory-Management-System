import { useState } from 'react';
import { Button, Card, Form, Input, message, Typography } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabaseClient';

const { Title, Text } = Typography;

const Register = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values: { email: string; password: string }) => {
    setLoading(true);
    const { email, password } = values;
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        // 若开启邮件验证，需在 Supabase 控制台配置允许的 Redirect URL
        emailRedirectTo: window.location.origin + '/login',
      },
    });
    setLoading(false);
    if (error) {
      message.error(error.message || '注册失败');
      return;
    }
    message.success('注册成功，请查收验证邮件或直接登录');
    navigate('/login');
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
          账号注册
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
              注册
            </Button>
          </Form.Item>
          <Text type="secondary">
            已有账号？<Link to="/login">去登录</Link>
          </Text>
        </Form>
      </Card>
    </div>
  );
};

export default Register;
