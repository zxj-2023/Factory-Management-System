import { ReactElement } from 'react';
import { Navigate } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuth } from '../hooks/useAuth';

type Props = {
  element: ReactElement;
};

/**
 * 路由守卫：未登录跳转 /login，登录中显示加载。
 */
const ProtectedRoute = ({ element }: Props) => {
  const { session, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!session) {
    return <Navigate to="/login" replace />;
  }

  return element;
};

export default ProtectedRoute;
