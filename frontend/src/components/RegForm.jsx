import React, { useState } from 'react';
import { Button, Form, Input, Alert, message } from 'antd';
import axios from "axios";
import GoogleOauthButton from './GoogleButton.jsx';

function LoginForm({ onSuccess }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const onFinish = async (values) => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/login',
                {
                    login: values.login.trim(),
                    password: values.password
                },
                {
                    withCredentials: true,
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            if (response.data.ok) {
                message.success(response.data.detail);
                onSuccess();
            }
        } catch (err) {
            console.error('Login error:', err);
            setError(err.response?.data?.detail || 'Ошибка авторизации');
            message.error('Неверный логин или пароль');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md w-full mx-auto p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-center mb-6">Вход в систему</h2>

            {error && (
                <Alert
                    message="Ошибка авторизации"
                    description={error}
                    type="error"
                    showIcon
                    closable
                    className="mb-4"
                />
            )}

            <Form
                name="login"
                layout="vertical"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                autoComplete="off"
                className="space-y-4"
            >
                <Form.Item
                    label={<span className="text-gray-700 font-medium">Логин или Email</span>}
                    name="login"
                    rules={[
                        { required: true, message: 'Пожалуйста, введите логин или email!' },
                        { whitespace: true, message: 'Не может состоять только из пробелов' }
                    ]}
                    validateTrigger="onBlur"
                >
                    <Input
                        placeholder="Введите ваш логин или email"
                        className="w-full p-2 border border-gray-300 rounded-md hover:border-blue-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </Form.Item>

                <Form.Item
                    label={<span className="text-gray-700 font-medium">Пароль</span>}
                    name="password"
                    rules={[
                        { required: true, message: 'Пожалуйста, введите пароль!' },
                        { min: 8, message: 'Пароль должен быть не менее 6 символов' }
                    ]}
                >
                    <Input.Password
                        placeholder="Введите ваш пароль"
                        className="w-full p-2 border border-gray-300 rounded-md hover:border-blue-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </Form.Item>

                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                    >
                        Войти
                    </Button>
                </Form.Item>
            </Form>

            <div className="mt-6 text-center">
                <p className="text-gray-600 mb-4">Или войдите через</p>
                <GoogleOauthButton className="w-full justify-center" />
            </div>
        </div>
    );
}

export default LoginForm;
