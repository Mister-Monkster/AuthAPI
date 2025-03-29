import React, { useEffect, useState } from 'react';
import {Card, Form, Input, Alert, Typography, DatePicker, Button, message} from 'antd';
import {
    CheckCircleOutlined,
    ExclamationCircleOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';
import axios from "axios";
import TextArea from "antd/es/input/TextArea.js";

const { Text } = Typography;

const ProfileView = ({ userData }) => {
    return (
        <div className='gap-3 flex-col w-md p-3'>
            <h2 className="text-2xl font-bold mb-4">Мой профиль</h2>

            {!userData.is_verificate && (
                <Alert
                    message="Требуется верификация"
                    description="Пожалуйста, завершите верификацию для полного доступа к функциям"
                    type="warning"
                    showIcon
                    style={{ marginBottom: 24 }}
                />
            )}

            <div style={{ marginBottom: 16 }}>
                <Text strong>Статус верификации: </Text>
                {userData.is_verificate ? (
                    <Text type="success">
                        <CheckCircleOutlined style={{ color: '#52c41a' }} /> Верифицирован
                    </Text>
                ) : (
                    <Text type="warning">
                        <ExclamationCircleOutlined style={{ color: '#faad14' }} /> Не верифицирован
                    </Text>
                )}
            </div>

            <div className="profile-info">
                <p><strong>Имя пользователя:</strong> {userData.username || 'Не указано'}</p>
                <p><strong>Email:</strong> {userData.email || 'Не указано'}</p>
                <p><strong>Телефон:</strong> {userData.phone || 'Не указано'}</p>
                <p><strong>О себе:</strong> {userData.bio || 'Не указано'}</p>
                <p><strong>Город:</strong> {userData.city || 'Не указано'}</p>
                <p><strong>Улица:</strong> {userData.street || 'Не указано'}</p>
                <p><strong>Дом:</strong> {userData.home || 'Не указано'}</p>
                <p><strong>Квартира:</strong> {userData.flat || 'Не указано'}</p>
                <p><strong>Дата рождения:</strong> {userData.birth || 'Не указано'}</p>
            </div>
        </div>
    );
};

const EditProfileForm = ({ userData, onSave }) => {
    const [form] = Form.useForm();

    useEffect(() => {
        if (userData) {
            form.setFieldsValue({
                ...userData,
                birth: userData.birth ? dayjs(userData.birth) : null
            });
        }
    }, [userData, form]);

    const handleSubmit = (values) => {
        const dataToSend = {
            ...values,
            birth: values.birth ? dayjs(values.birth).format('YYYY-MM-DD') : null
        };
        onSave(dataToSend);
    };

    return (
        <div className='gap-3 flex-col w-md p-3'>
            <h2 className="text-2xl font-bold mb-4">Изменить данные</h2>

            <Form
                form={form}
                className="w-full max-w-md"
                onFinish={handleSubmit}
                initialValues={{
                    ...userData,
                    birth: userData.birth ? dayjs(userData.birth) : null
                }}
            >
                <Form.Item
                    name="username"
                    label='Имя пользователя'
                    rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="email"
                    label="Email"
                    rules={[{ required: true, message: 'Пожалуйста, введите email!' }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="phone"
                    label="Телефон"
                    rules={[{ required: true, message: 'Пожалуйста, введите номер телефона!' }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="bio"
                    label="О себе"
                >
                    <TextArea />
                </Form.Item>
                <Form.Item name="city" label='Город'>
                    <Input placeholder="Не указано" />
                </Form.Item>
                <Form.Item name="street" label='Улица'>
                    <Input placeholder="Не указано" />
                </Form.Item>
                <Form.Item name="home" label='Дом'>
                    <Input placeholder="Не указано" />
                </Form.Item>
                <Form.Item name="flat" label='Квартира'>
                    <Input placeholder="Не указано" />
                </Form.Item>
                <Form.Item name="birth" label='Дата рождения'>
                    <DatePicker
                        format="YYYY-MM-DD"
                        style={{ width: '100%' }}
                    />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Сохранить изменения
                    </Button>
                </Form.Item>
                <Form.Item name="is_verificate" hidden>
                    <Input type="hidden" />
                </Form.Item>
            </Form>
        </div>
    );
};

const ChangePasswordForm = () => {
    const [form] = Form.useForm(); // 1. Создаём экземпляр формы

    const handleSave = async (values) => {
        try {
            const response = await axios.put(
                'http://localhost:8000/user/update-password',
                values,
                {
                    withCredentials: true,
                    headers: { 'Content-Type': 'application/json' },
                }
            );


            if (response.data && response.data.ok) {
                message.success('Пароль успешно изменён!');
                form.resetFields();
                setTimeout(() => {
                    window.location.reload(); // Или другой способ обновления данных
                }, 1500); // Небольшая задержка для UX


                setTimeout(() => {
                    form.resetFields();
                }, 0);
            } else {
                message.error(response.data?.detail || 'Ошибка изменения пароля');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            message.error(error.response?.data?.detail || 'Произошла ошибка');

        }
    };


    return (
        <div className='gap-3 flex-col w-md p-3'>
            <h2 className="text-2xl font-bold mb-4">Изменить пароль</h2>
            <Form
                form={form}
                className="w-full max-w-md"
                onFinish={handleSave}
            >
                <Form.Item
                    label={<span className="text-gray-700 font-medium">Пароль</span>}
                    name="old_password"
                    rules={[
                        { required: true, message: 'Пожалуйста, введите пароль!' },
                        { min: 8, message: 'Пароль должен быть не менее 6 символов' }
                    ]}
                >
                    <Input.Password
                        placeholder="Введите ваш текущий пароль"
                        className="w-full p-2 border border-gray-300 rounded-md hover:border-blue-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </Form.Item>
                <Form.Item
                    label={<span className="text-gray-700 font-medium">Новый пароль</span>}
                    name="new_password"
                    rules={[
                        { required: true, message: 'Пожалуйста, введите пароль!' },
                        { min: 8, message: 'Пароль должен быть не менее 8 символов' }
                    ]}
                >
                    <Input.Password
                        placeholder="Введите ваш новый пароль"
                        className="w-full p-2 border border-gray-300 rounded-md hover:border-blue-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </Form.Item>
                <Form.Item
                    label={<span className="text-gray-700 font-medium">Подтверждение пароля</span>}
                    name="confirm_new_password"
                    rules={[
                        { required: true, message: 'Пожалуйста, введите пароль!' },
                        { min: 8, message: 'Пароль должен быть не менее 8 символов' }
                    ]}
                >
                    <Input.Password
                        placeholder="Подтвердите ваш новый пароль"
                        className="w-full p-2 border border-gray-300 rounded-md hover:border-blue-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Изменить пароль
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

const ProfileForm = ({ userData }) => {
    const [activeTabKey, setActiveTabKey] = useState('tab1');

    const handleSave = async (values) => {
        try {
            const response = await axios.put(
                'http://localhost:8000/user/update',
                values,
                {
                    withCredentials: true,
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            if (response.data.ok) {
                console.log('Данные успешно обновлены!');
                return response.data;}
        } catch (error) {
            console.error('Ошибка:', error);
            throw error;
        }
    };

    const tabList = [
        {
            key: 'tab1',
            tab: 'Мой профиль',
        },
        {
            key: 'tab2',
            tab: 'Изменить данные',
        },
        {
            key: 'tab3',
            tab: 'Изменить пароль'
        }
    ];

    const contentList = {
        tab1: <ProfileView userData={userData} />,
        tab2: <EditProfileForm userData={userData} onSave={handleSave} />,
        tab3: <ChangePasswordForm onSave={handleSave} />,
    };

    const onTabChange = (key) => {
        setActiveTabKey(key);
    };

    return (
        <Card
            style={{ width: '100%' }}
            title="Профиль пользователя"
            tabList={tabList}
            activeTabKey={activeTabKey}
            onTabChange={onTabChange}
        >
            {contentList[activeTabKey]}
        </Card>
    );
};

export default ProfileForm;