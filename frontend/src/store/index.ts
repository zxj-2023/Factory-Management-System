import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {
    // 将在这里添加各个 slice
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;