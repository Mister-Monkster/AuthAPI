import React, { useEffect, useState } from 'react';
import {
    MenuFoldOutlined,
    MenuUnfoldOutlined,
    TeamOutlined,
    UserOutlined,
    LoginOutlined,
    LogoutOutlined,
    FormOutlined,
    SafetyOutlined,
    CheckCircleOutlined,
    ExclamationCircleOutlined
} from '@ant-design/icons';
import { Alert, Menu } from 'antd';
import axios from "axios";
import RegForm from "./components/RegForm";
import LoginForm from "./components/RegistrationForm.jsx";
import VerifyForm from "./components/VerifyForm";
import ProfileForm from "./components/ProfileForm";
import UserCards from "./components/UsersCards"; // Импортируем компонент UserCards

const App = () => {
    const [userData, setUserData] = useState(null);
    const [collapsed, setCollapsed] = useState(false);
    const [activeForm, setActiveForm] = useState(null);
    const [alertMessage, setAlertMessage] = useState(null);
    const [showUsers, setShowUsers] = useState(false); // Добавляем состояние для отображения списка пользователей

    const fetchCurrentUser = async () => {
        try {
            const response = await axios.get("http://localhost:8000/my-profile", {
                headers: { 'Content-Type': 'application/json' },
                withCredentials: true,
            });

            if (response.status === 200) {
                setUserData(response.data);
                setAlertMessage({
                    type: 'success',
                    text: `Вы успешно вошли как ${response.data.username}`,
                });

                if (!response.data.is_verificate) {
                    setActiveForm('verify');
                } else {
                    setActiveForm('profile');
                }
            }
        } catch (error) {
            if (error.response?.status === 401) {
                try {
                    const refreshResponse = await axios.post(
                        "http://localhost:8000/refresh",
                        {},
                        {
                            headers: { 'Content-Type': 'application/json' },
                            withCredentials: true,
                        }
                    );

                    if (refreshResponse.status === 200) {
                        fetchCurrentUser();
                    }
                } catch (refreshError) {
                    setAlertMessage({
                        type: 'error',
                        text: 'Вы не авторизованы',
                    });
                    setActiveForm('login');
                }
            } else {
                setAlertMessage({
                    type: 'error',
                    text: error.response?.data?.detail || 'Ошибка при входе',
                });
                setActiveForm('login');
            }
        }
    };

    useEffect(() => {
        fetchCurrentUser();
    }, []);

    useEffect(() => {
        if (activeForm === null) {
            if (userData) {
                setActiveForm('profile');
            } else {
                setActiveForm('login');
            }
        }
    }, [userData, activeForm]);

    const logout = async () => {
        try {
            await axios.post(
                "http://localhost:8000/logout",
                {},
                {
                    withCredentials: true,
                    headers: { "Content-Type": "application/json" },
                }
            );
            setUserData(null);
            setActiveForm('login');
            setShowUsers(false); // Сбрасываем состояние при выходе
            setAlertMessage({
                type: 'success',
                text: 'Вы успешно вышли из системы',
            });
        } catch (error) {
            setAlertMessage({
                type: 'error',
                text: 'Ошибка при выходе из системы',
            });
            console.error('Ошибка при выходе:', error);
        }
    };

    const getMenuItems = () => {
        if (userData) {
            const items = [
                {
                    key: 'verification-status',
                    icon: userData.is_verificate ?
                        <CheckCircleOutlined className="text-lg" /> :
                        <ExclamationCircleOutlined className="text-lg" />,
                    label: userData.is_verificate ?
                        'Верифицирован' :
                        'Не верифицирован',
                    style: {
                        color: userData.is_verificate ? '#52c41a' : '#faad14',
                        cursor: 'default'
                    }
                },

                {
                    key: 'profile',
                    icon: <UserOutlined className="text-lg" />,
                    label: 'Мой профиль',
                    onClick: () => {
                        setActiveForm('profile');
                        setShowUsers(false);
                    }
                },

                {
                    key: 'users',
                    icon: <TeamOutlined className="text-lg" />,
                    label: 'Пользователи',
                    onClick: () => {
                        setShowUsers(true);
                        setActiveForm(null);
                    }
                }
            ];

            if (!userData.is_verificate) {
                items.splice(2, 0, {
                    key: 'verify',
                    icon: <SafetyOutlined className="text-lg" />,
                    label: 'Верификация',
                    onClick: () => {
                        setActiveForm('verify');
                        setShowUsers(false);
                    }
                });
            }

            items.push({
                key: 'logout',
                icon: <LogoutOutlined className="text-lg" />,
                label: 'Выйти',
                onClick: logout,
            });

            return items;
        }

        return [
            {
                key: 'register',
                icon: <FormOutlined className="text-lg" />,
                label: 'Зарегистрироваться',
                onClick: () => {
                    setActiveForm('register');
                    setShowUsers(false);
                }
            },
            {
                key: 'login',
                icon: <LoginOutlined className="text-lg" />,
                label: 'Войти',
                onClick: () => {
                    setActiveForm('login');
                    setShowUsers(false);
                }
            },
        ];
    };

    const renderContent = () => {
        if (showUsers) {
            return <UserCards />;
        }

        if (!userData) {
            return activeForm === 'register' ? (
                <LoginForm
                    onSuccess={fetchCurrentUser}
                    onSwitchToRegister={() => setActiveForm('register')}
                />
            ) : (
                <RegForm
                    onSuccess={fetchCurrentUser}
                    onSwitchToLogin={() => setActiveForm('login')}
                />
            );
        }

        if (activeForm === 'verify' && !userData.is_verificate) {
            return (
                <div className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
                    <h2 className="text-2xl font-bold mb-4">Верификация аккаунта</h2>
                    <VerifyForm
                        onSuccess={() => {
                            fetchCurrentUser();
                            setActiveForm('profile');
                        }}
                        userEmail={userData.email}
                    />
                </div>
            );
        }

        if (activeForm === 'profile') {
            return <ProfileForm userData={userData} />;
        }

        return null;
    };

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <div className={`bg-gray-800 text-white transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'}`}>
                <div className="flex items-center justify-between p-4 border-b border-gray-700">
                    {!collapsed && <h1 className="text-xl font-bold">Меню</h1>}
                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        className="text-gray-300 hover:text-white"
                    >
                        {collapsed ? <MenuUnfoldOutlined className="text-xl" /> : <MenuFoldOutlined className="text-xl" />}
                    </button>
                </div>
                <Menu
                    theme="dark"
                    mode="inline"
                    selectedKeys={[showUsers ? 'users' : activeForm]}
                    items={getMenuItems()}
                    className="border-none"
                />
            </div>

            {/* Main Content */}
            <div className="flex-1 overflow-auto">
                <div className="min-h-full">
                    <div className="flex justify-center p-6">
                        <div className="w-full max-w-4xl">
                            {renderContent()}
                        </div>
                    </div>
                </div>

                {/* Alert Notification */}
                {alertMessage && (
                    <div className="fixed bottom-4 right-4 z-50">
                        <Alert
                            message={alertMessage.text}
                            type={alertMessage.type}
                            showIcon
                            closable
                            onClose={() => setAlertMessage(null)}
                            className="w-64 shadow-lg"
                        />
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;