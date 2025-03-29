import React from 'react';
import { Button, Form, Input, message as antdMessage } from 'antd';
import axios from "axios";
import GoogleOauthButton from './GoogleButton.jsx';

const API_BASE_URL = 'http://localhost:8000';

function RegistrationForm({ onSuccess }) {
    const [form] = Form.useForm();
    const [loading, setLoading] = React.useState(false);

    const onFinish = async (values) => {
        if (values.password !== values.confirm) {
            antdMessage.error('Пароли не совпадают!');
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post(`${API_BASE_URL}/registration`, values, {
                withCredentials: true,
                headers: { 'Content-Type': 'application/json' },
            });

            if (response.status === 200) {
                antdMessage.success('Регистрация прошла успешно!');
                onSuccess();
            }
        } catch (error) {
            if (error.response?.status === 422) {
                antdMessage.error(error.response.data?.detail || 'Ошибка валидации');
            } else {
                antdMessage.error('Ошибка регистрации. Пожалуйста, попробуйте снова.');
            }
            console.error('Ошибка регистрации:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
            <h1 className="text-2xl font-bold text-center mb-6">Регистрация</h1>

            <Form
                form={form}
                layout="vertical"
                onFinish={onFinish}
                autoComplete="off"
                className="space-y-4"
            >
                {/* Личная информация */}
                <div className="space-y-4">
                    <Form.Item
                        label="Имя пользователя"
                        name="username"
                        rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
                    >
                        <Input className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                            { required: true, message: 'Пожалуйста, введите email!' },
                            { type: 'email', message: 'Неверный формат email' }
                        ]}
                    >
                        <Input className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item
                        label="Пароль"
                        name="password"
                        rules={[{ required: true, message: 'Пожалуйста, введите пароль!' }]}
                    >
                        <Input.Password className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item
                        label="Подтверждение пароля"
                        name="confirm"
                        rules={[{ required: true, message: 'Пожалуйста, подтвердите пароль!' }]}
                    >
                        <Input.Password className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item
                        label="Номер телефона"
                        name="phone"
                        rules={[{ required: true, message: 'Пожалуйста, введите номер телефона!' }]}
                    >
                        <Input className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item label="Дата рождения" name="birth">
                        <Input type="date" className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item label="О себе" name="bio">
                        <Input.TextArea className="w-full p-2 border rounded" rows={3} />
                    </Form.Item>
                </div>

                {/* Адрес */}
                <div className="mt-6 space-y-4">
                    <h2 className="text-lg font-semibold">Адрес</h2>

                    <Form.Item label="Город" name="city">
                        <Input className="w-full p-2 border rounded" />
                    </Form.Item>

                    <Form.Item label="Улица" name="street">
                        <Input className="w-full p-2 border rounded" />
                    </Form.Item>

                    <div className="grid grid-cols-2 gap-4">
                        <Form.Item label="Дом" name="home">
                            <Input className="w-full p-2 border rounded" />
                        </Form.Item>
                        <Form.Item label="Квартира" name="flat">
                            <Input className="w-full p-2 border rounded" />
                        </Form.Item>
                    </div>
                </div>

                <Form.Item className="mt-8">
                    <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Зарегистрироваться
                    </Button>
                </Form.Item>
            </Form>

            <div className="mt-6 text-center">
                <p className="text-gray-600 mb-4">Или зарегистрируйтесь через</p>
                <GoogleOauthButton />
            </div>
        </div>
    );
}

export default RegistrationForm;