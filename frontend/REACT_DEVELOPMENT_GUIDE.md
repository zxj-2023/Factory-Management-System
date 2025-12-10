# React 开发指南 - 新手入门

这是一份专为初学者准备的 React 开发指南，帮助你快速上手 React 开发。

## 📚 目录

1. [React 基础概念](#react-基础概念)
2. [项目结构解析](#项目结构解析)
3. [常用 Hook 详解](#常用-hook-详解)
4. [组件开发实践](#组件开发实践)
5. [状态管理](#状态管理)
6. [样式处理](#样式处理)
7. [API 调用](#api-调用)
8. [路由使用](#路由使用)
9. [表单处理](#表单处理)
10. [常见问题解决](#常见问题解决)

## React 基础概念

### 1. 什么是组件？

组件是 React 应用的基本构建块，就像搭积木一样。

```typescript
// 函数组件示例
const WelcomeMessage = () => {
  return <h1>欢迎使用 React!</h1>;
};

// 带有属性的组件
const Greeting = ({ name, age }) => {
  return (
    <div>
      <p>你好，{name}!</p>
      <p>你今年 {age} 岁了。</p>
    </div>
  );
};

// 使用组件
const App = () => {
  return (
    <div>
      <WelcomeMessage />
      <Greeting name="张三" age={25} />
    </div>
  );
};
```

### 2. JSX 语法

JSX 是 JavaScript 的扩展，让你可以在 JS 中写类似 HTML 的代码。

```typescript
const element = <h1>Hello, world!</h1>;

// 使用变量
const name = 'Josh Perez';
const element = <h1>Hello, {name}</h1>;

// 使用表达式
const element = <h1>The result is {2 + 2}</h1>;

// 使用条件渲染
const user = { isLoggedIn: true };
const element = (
  <div>
    {user.isLoggedIn ? <h1>Welcome back!</h1> : <h1>Please sign up.</h1>}
  </div>
);
```

## 项目结构解析

```
src/
├── components/      # 可复用组件
├── pages/          # 页面组件
├── services/       # API 服务
├── store/          # Redux 状态管理
├── types/          # TypeScript 类型定义
├── hooks/          # 自定义 Hooks
├── utils/          # 工具函数
├── App.tsx         # 主应用组件
├── index.tsx       # 应用入口
└── index.css       # 全局样式
```

### 各目录详细说明

#### components/ - 可复用组件
存放可以在多个地方使用的组件：

```typescript
// components/Button.tsx
import React from 'react';
import { Button as AntButton } from 'antd';

interface ButtonProps {
  type?: 'primary' | 'default' | 'danger';
  onClick?: () => void;
  children: React.ReactNode;
}

const CustomButton = ({ type = 'primary', onClick, children }: ButtonProps) => {
  return (
    <AntButton type={type} onClick={onClick}>
      {children}
    </AntButton>
  );
};

export default CustomButton;
```

#### pages/ - 页面组件
每个页面对应一个路由：

```typescript
// pages/HomePage.tsx
import React from 'react';
import CustomButton from '../components/Button';

const HomePage = () => {
  const handleClick = () => {
    alert('按钮被点击了！');
  };

  return (
    <div>
      <h1>首页</h1>
      <CustomButton onClick={handleClick}>点击我</CustomButton>
    </div>
  );
};

export default HomePage;
```

## 常用 Hook 详解

### 1. useState - 状态管理

```typescript
import React, { useState } from 'react';

const Counter = () => {
  // 声明一个状态变量
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(count + 1);
  };

  const decrement = () => {
    setCount(count - 1);
  };

  return (
    <div>
      <p>当前计数: {count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
    </div>
  );
};
```

### 2. useEffect - 副作用处理

```typescript
import React, { useState, useEffect } from 'react';

const DataFetcher = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 组件挂载后执行
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('https://api.example.com/data');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('获取数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // 组件卸载时执行（清理函数）
    return () => {
      console.log('组件即将卸载');
    };
  }, []); // 空数组表示只在挂载时执行一次

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div>
      <h2>数据列表</h2>
      <ul>
        {data.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
};
```

### 3. useContext - 共享数据

```typescript
import React, { createContext, useContext, useState } from 'react';

// 创建上下文
const ThemeContext = createContext();

// 主题提供者组件
const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// 使用主题的组件
const ThemedButton = () => {
  const { theme, setTheme } = useContext(ThemeContext);

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <button
      style={{
        backgroundColor: theme === 'light' ? '#fff' : '#333',
        color: theme === 'light' ? '#333' : '#fff'
      }}
      onClick={toggleTheme}
    >
      切换主题
    </button>
  );
};
```

## 组件开发实践

### 1. 组件传参

```typescript
// 父组件
const ParentComponent = () => {
  const [user, setUser] = useState({
    name: '张三',
    age: 25,
    email: 'zhangsan@example.com'
  });

  const updateUser = (newName: string) => {
    setUser({ ...user, name: newName });
  };

  return (
    <div>
      <ChildComponent
        user={user}
        onUpdate={updateUser}
        isLoggedIn={true}
      />
    </div>
  );
};

// 子组件
interface ChildComponentProps {
  user: {
    name: string;
    age: number;
    email: string;
  };
  onUpdate: (name: string) => void;
  isLoggedIn: boolean;
}

const ChildComponent = ({ user, onUpdate, isLoggedIn }: ChildComponentProps) => {
  return (
    <div>
      <h3>用户信息</h3>
      <p>姓名: {user.name}</p>
      <p>年龄: {user.age}</p>
      <p>邮箱: {user.email}</p>
      <p>状态: {isLoggedIn ? '已登录' : '未登录'}</p>

      <button onClick={() => onUpdate('李四')}>
        修改姓名
      </button>
    </div>
  );
};
```

### 2. 条件渲染

```typescript
const ConditionalComponent = ({ user, loading }) => {
  if (loading) {
    return <div>加载中...</div>;
  }

  if (!user) {
    return <div>用户不存在</div>;
  }

  return (
    <div>
      {user.isAdmin && <AdminPanel />}
      {user.age >= 18 ? <AdultContent /> : <MinorContent />}
    </div>
  );
};

// 或者使用三元运算符
const Greeting = ({ isLogin }) => {
  return (
    <div>
      {isLogin ? <WelcomeBack /> : <PleaseLogin />}
    </div>
  );
};
```

### 3. 列表渲染

```typescript
const TodoList = () => {
  const [todos, setTodos] = useState([
    { id: 1, text: '学习 React', completed: false },
    { id: 2, text: '完成项目', completed: true },
    { id: 3, text: '写文档', completed: false }
  ]);

  const toggleTodo = (id: number) => {
    setTodos(todos.map(todo =>
      todo.id === id
        ? { ...todo, completed: !todo.completed }
        : todo
    ));
  };

  return (
    <div>
      <h2>待办事项</h2>
      <ul>
        {todos.map(todo => (
          <li
            key={todo.id}
            onClick={() => toggleTodo(todo.id)}
            style={{
              textDecoration: todo.completed ? 'line-through' : 'none',
              cursor: 'pointer'
            }}
          >
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

## 状态管理

### 1. 本地状态（useState）

```typescript
const FormComponent = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <form>
      <input
        type="text"
        placeholder="用户名"
        value={formData.username}
        onChange={(e) => handleChange('username', e.target.value)}
      />
      <input
        type="email"
        placeholder="邮箱"
        value={formData.email}
        onChange={(e) => handleChange('email', e.target.value)}
      />
      <input
        type="password"
        placeholder="密码"
        value={formData.password}
        onChange={(e) => handleChange('password', e.target.value)}
      />
    </form>
  );
};
```

### 2. 使用 Redux Toolkit

```typescript
// store/slices/counterSlice.ts
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: {
    value: 0
  },
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    }
  }
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;

// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer
  }
});

// 在组件中使用
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from '../store/slices/counterSlice';

const CounterComponent = () => {
  const count = useSelector(state => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <p>计数: {count}</p>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>
    </div>
  );
};
```

## 样式处理

### 1. CSS 模块

```css
/* Button.module.css */
.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.primary {
  background-color: #1890ff;
  color: white;
}

.secondary {
  background-color: #f0f0f0;
  color: #333;
}
```

```typescript
// Button.tsx
import styles from './Button.module.css';

const Button = ({ type = 'primary', children, onClick }) => {
  return (
    <button
      className={`${styles.button} ${styles[type]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### 2. 行内样式

```typescript
const StyledComponent = () => {
  const style = {
    container: {
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px'
    },
    title: {
      color: '#1890ff',
      fontSize: '24px',
      marginBottom: '16px'
    }
  };

  return (
    <div style={style.container}>
      <h1 style={style.title}>标题</h1>
      <p>内容...</p>
    </div>
  );
};
```

### 3. 使用 Ant Design

```typescript
import { Button, Table, Form, Input, Select, Space } from 'antd';

const UserManagement = () => {
  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '年龄',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button type="primary">编辑</Button>
          <Button type="danger" danger>删除</Button>
        </Space>
      ),
    },
  ];

  const data = [
    { key: '1', name: '张三', age: 32 },
    { key: '2', name: '李四', age: 42 },
  ];

  return (
    <div>
      <Table columns={columns} dataSource={data} />
    </div>
  );
};
```

## API 调用

### 1. 使用 Fetch API

```typescript
const useApi = (url: string) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('网络请求失败');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
};

// 使用
const UserList = () => {
  const { data: users, loading, error } = useApi('/api/users');

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误: {error}</div>;

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

### 2. 使用 Axios

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// 使用示例
const userService = {
  getAll: () => api.get('/users'),
  getById: (id: number) => api.get(`/users/${id}`),
  create: (data: any) => api.post('/users', data),
  update: (id: number, data: any) => api.put(`/users/${id}`, data),
  delete: (id: number) => api.delete(`/users/${id}`)
};
```

## 路由使用

### 1. 基础路由配置

```typescript
// App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import NotFoundPage from './pages/NotFoundPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};
```

### 2. 动态路由

```typescript
// App.tsx
<Routes>
  <Route path="/users/:id" element={<UserDetail />} />
  <Route path="/posts/:category/:postId" element={<PostDetail />} />
</Routes>

// UserDetail.tsx
import { useParams } from 'react-router-dom';

const UserDetail = () => {
  const { id } = useParams();

  return <div>用户详情页 - ID: {id}</div>;
};
```

### 3. 导航

```typescript
import { Link, useNavigate } from 'react-router-dom';

const Navigation = () => {
  const navigate = useNavigate();

  const handleGoToAbout = () => {
    navigate('/about');
  };

  return (
    <nav>
      <Link to="/">首页</Link>
      <Link to="/about">关于</Link>
      <button onClick={handleGoToAbout}>跳转到关于页</button>
    </nav>
  );
};
```

## 表单处理

### 1. 受控组件

```typescript
const ControlledForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [field]: e.target.value });
    // 清除对应字段的错误
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username) {
      newErrors.username = '用户名不能为空';
    }

    if (!formData.email) {
      newErrors.email = '邮箱不能为空';
    } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = '邮箱格式不正确';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = '两次输入的密码不一致';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      console.log('表单数据:', formData);
      // 提交表单
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          placeholder="用户名"
          value={formData.username}
          onChange={handleChange('username')}
        />
        {errors.username && <span style={{ color: 'red' }}>{errors.username}</span>}
      </div>

      <div>
        <input
          type="email"
          placeholder="邮箱"
          value={formData.email}
          onChange={handleChange('email')}
        />
        {errors.email && <span style={{ color: 'red' }}>{errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="密码"
          value={formData.password}
          onChange={handleChange('password')}
        />
      </div>

      <div>
        <input
          type="password"
          placeholder="确认密码"
          value={formData.confirmPassword}
          onChange={handleChange('confirmPassword')}
        />
        {errors.confirmPassword && (
          <span style={{ color: 'red' }}>{errors.confirmPassword}</span>
        )}
      </div>

      <button type="submit">提交</button>
    </form>
  );
};
```

### 2. 使用 Ant Design Form

```typescript
import { Form, Input, Button, Select } from 'antd';

const AntForm = () => {
  const [form] = Form.useForm();

  const onFinish = (values) => {
    console.log('表单值:', values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log('表单验证失败:', errorInfo);
  };

  return (
    <Form
      form={form}
      name="basic"
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="off"
    >
      <Form.Item
        label="用户名"
        name="username"
        rules={[
          { required: true, message: '请输入用户名!' },
          { min: 3, message: '用户名至少3个字符!' }
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="密码"
        name="password"
        rules={[
          { required: true, message: '请输入密码!' },
          { min: 6, message: '密码至少6个字符!' }
        ]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        label="性别"
        name="gender"
        rules={[{ required: true, message: '请选择性别!' }]}
      >
        <Select>
          <Select.Option value="male">男</Select.Option>
          <Select.Option value="female">女</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
        <Button type="primary" htmlType="submit">
          提交
        </Button>
      </Form.Item>
    </Form>
  );
};
```

## 常见问题解决

### 1. 组件不重新渲染

```typescript
// 错误示例 - 直接修改状态
const WrongComponent = () => {
  const [list, setList] = useState([1, 2, 3]);

  const addItem = () => {
    // 直接修改数组，组件不会重新渲染
    list.push(4);
    setList(list);
  };

  return <button onClick={addItem}>添加项目</button>;
};

// 正确示例 - 创建新的对象/数组
const CorrectComponent = () => {
  const [list, setList] = useState([1, 2, 3]);

  const addItem = () => {
    // 使用展开运算符创建新数组
    setList([...list, 4]);
  };

  return <button onClick={addItem}>添加项目</button>;
};
```

### 2. useEffect 中的依赖问题

```typescript
// 错误示例 - 缺少依赖
const WrongComponent = ({ userId }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []); // 缺少 userId 依赖

  return <div>{user?.name}</div>;
};

// 正确示例 - 包含所有依赖
const CorrectComponent = ({ userId }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]); // 包含所有外部依赖

  return <div>{user?.name}</div>;
};
```

### 3. 记忆化优化

```typescript
import React, { useState, useMemo, useCallback } from 'react';

const ExpensiveComponent = ({ data }) => {
  // 使用 useMemo 缓存计算结果
  const expensiveValue = useMemo(() => {
    console.log('执行复杂计算...');
    return data.reduce((sum, num) => sum + num, 0);
  }, [data]); // 只有 data 改变时才重新计算

  // 使用 useCallback 缓存函数
  const handleClick = useCallback(() => {
    console.log('点击事件', expensiveValue);
  }, [expensiveValue]); // 只有 expensiveValue 改变时才创建新函数

  return (
    <div>
      <p>计算结果: {expensiveValue}</p>
      <button onClick={handleClick}>点击</button>
    </div>
  );
};
```

### 4. 处理异步操作

```typescript
const AsyncComponent = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 使用 async/await 处理异步
      const response = await fetch('/api/data');

      if (!response.ok) {
        throw new Error('请求失败');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={fetchData} disabled={loading}>
        {loading ? '加载中...' : '获取数据'}
      </button>

      {error && <div style={{ color: 'red' }}>错误: {error}</div>}

      <ul>
        {data.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
};
```

## 开发建议

### 1. 组件设计原则
- **单一职责**: 每个组件只做一件事
- **保持纯净**: 相同输入总是产生相同输出
- **适当拆分**: 大组件拆分成小组件

### 2. 性能优化
- 使用 React.memo 避免不必要的渲染
- 合理使用 useMemo 和 useCallback
- 避免在 render 中创建新对象/函数

### 3. 代码组织
- 相关的组件放在一起
- 使用清晰的命名
- 添加适当的注释

### 4. 调试技巧
- 使用 React DevTools
- 使用 console.log 调试
- 利用 TypeScript 类型检查

## 总结

React 开发需要掌握的核心概念：
1. **组件化思维** - 将 UI 拆分成可复用的组件
2. **状态管理** - 合理使用 useState、useEffect、useContext
3. **生命周期** - 理解组件的挂载、更新、卸载
4. **数据流** - 单向数据流，props 向下传递
5. **性能优化** - 避免不必要的重渲染

记住，React 的学习曲线可能有些陡峭，但通过不断练习和实践，你会逐渐掌握它的精髓。祝你开发愉快！

---

*这份文档会根据你的学习进度不断更新和完善。*