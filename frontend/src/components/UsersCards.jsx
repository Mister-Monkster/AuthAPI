import React, { useState, useEffect } from 'react';
import { Card, Pagination, Spin, message } from 'antd';
import axios from "axios";

const PAGE_SIZE = 10;

const UserCards = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalUsers, setTotalUsers] = useState(0);

    const fetchUsers = async (page = 1) => {
        try {
            setLoading(true);
            const offset = (page - 1) * PAGE_SIZE;

            const response = await axios.get('http://localhost:8000/users', {
                params: { offset },
                withCredentials: true,
                headers: { 'Content-Type': 'application/json' },
            });

            setUsers(response.data.users);
            setTotalUsers(response.data.total);
        } catch (error) {
            message.error(error.response?.data?.detail || 'Ошибка загрузки');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchUsers(1); }, []);

    return (
        <div className="p-6">
            {loading ? (
                <div className="flex justify-center mt-20">
                    <Spin size="large" />
                </div>
            ) : (
                <div className="space-y-4">
                    {/* Одна карточка на всю ширину */}
                    <div className="space-y-4 w-full">
                        {users.map((user, index) => (
                            <Card
                                key={index}
                                title={
                                    <span className="text-lg font-semibold">
                                        {user.username}
                                    </span>
                                }
                                className="w-full shadow-md hover:shadow-lg transition-shadow"
                                headStyle={{ borderBottom: '1px solid #f0f0f0' }}
                                bodyStyle={{ padding: '16px 24px' }}
                            >
                                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                                    <div>
                                        <p className="text-gray-600">
                                            <span className="font-medium">Био:</span> {user.bio || '—'}
                                        </p>
                                    </div>
                                    <div>
                                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                                            user.is_verificate
                                                ? 'bg-green-100 text-green-800'
                                                : 'bg-yellow-100 text-yellow-800'
                                        }`}>
                                            {user.is_verificate ? (
                                                <>
                                                    <span className="mr-1">✓</span> Верифицирован
                                                </>
                                            ) : (
                                                <>
                                                    <span className="mr-1">×</span> Не верифицирован
                                                </>
                                            )}
                                        </span>
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>

                    {totalUsers > 0 && (
                        <div className="mt-6 text-center">
                            <Pagination
                                current={currentPage}
                                total={totalUsers}
                                pageSize={PAGE_SIZE}
                                onChange={(page) => {
                                    setCurrentPage(page);
                                    fetchUsers(page);
                                }}
                                className="inline-block"
                                showSizeChanger={false}
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default UserCards;