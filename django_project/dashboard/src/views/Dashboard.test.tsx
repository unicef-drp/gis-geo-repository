import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '../app/store';
import Dashboard from './Dashboard';

test('renders learn react link', () => {
  const { getByText } = render(
    <Provider store={store}>
      <Dashboard />
    </Provider>
  );

  expect(getByText(/test/i)).toBeInTheDocument();
});
