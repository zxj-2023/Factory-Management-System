import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { store } from './store';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Parts from './pages/Parts';
import Suppliers from './pages/Suppliers';
import Warehouses from './pages/Warehouses';
import Staff from './pages/Staff';
import Inventory from './pages/Inventory';
import Purchases from './pages/Purchases';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  return (
    <Provider store={store}>
      <ConfigProvider locale={zhCN}>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              element={<ProtectedRoute element={<Layout />} />}
            >
              <Route path="/" element={<Dashboard />} />
              <Route path="/parts" element={<Parts />} />
              <Route path="/suppliers" element={<Suppliers />} />
              <Route path="/warehouses" element={<Warehouses />} />
              <Route path="/staff" element={<Staff />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/purchases" element={<Purchases />} />
            </Route>
          </Routes>
        </Router>
      </ConfigProvider>
    </Provider>
  );
}

export default App;
