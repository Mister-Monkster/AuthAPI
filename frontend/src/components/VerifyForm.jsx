import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Form, Input, Button, message, Typography } from 'antd';

const { Text } = Typography;

const VerifyForm = ({ onSuccess, userEmail }) => {
    const [loading, setLoading] = useState(false);
    const [codeLoading, setCodeLoading] = useState(false);
    const [countdown, setCountdown] = useState(0);
    const [form] = Form.useForm();

    useEffect(() => {
        let timer;
        if (countdown > 0) {
            timer = setTimeout(() => setCountdown(c => c - 1), 1000);
        }
        return () => clearTimeout(timer);
    }, [countdown]);

    useEffect(() => {
        form.setFieldsValue({ code: '' });
        const input = document.getElementById('verificationCode');
        input?.focus();
    }, [form]);

    const handleVerification = useCallback(async (code) => {
        try {
            setLoading(true);
            const { data } = await axios.post(
                'http://localhost:8000/verification',
                { code: code },
                {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                }
            );

            if (data?.ok) {
                message.success(data.detail || 'Верификация прошла успешно!');
                onSuccess?.();
                return true;
            } else {
                message.error(data?.detail || 'Неверный код верификации');
                form.setFields([{ name: 'code', errors: [data?.detail || 'Неверный код'] }]);
                return false;
            }
        } catch (error) {
            handleVerificationError(error);
            return false;
        } finally {
            setLoading(false);
        }
    }, [form, onSuccess]);

    const handleVerificationError = (error) => {
        if (axios.isAxiosError(error)) {
            if (error.response) {
                const { status, data } = error.response;
                switch (status) {
                    case 401:
                        message.error('Сессия истекла. Пожалуйста, войдите снова.');
                        break;
                    case 422:
                        message.error(data?.detail || 'Неверный формат кода. Введите 6 цифр.');
                        break;
                    default:
                        message.error(data?.detail || 'Ошибка сервера при верификации');
                }
            } else if (error.request) {
                message.error('Нет ответа от сервера');
            } else {
                message.error('Ошибка при настройке запроса');
            }
        } else {
            message.error('Неизвестная ошибка');
        }
    };

    const handleResendCode = useCallback(async () => {
        if (countdown > 0) return;

        try {
            setCodeLoading(true);
            const { data } = await axios.post(
                'http://localhost:8000/code-retry',
                {},
                {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                }
            );

            message.success(data?.detail || `Новый код отправлен на ${userEmail}`);
            setCountdown(60);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                message.error(error.response?.data?.detail || 'Ошибка при отправке кода');
            } else {
                message.error('Неизвестная ошибка');
            }
        } finally {
            setCodeLoading(false);
        }
    }, [countdown, userEmail]);

    const onFinish = useCallback(async ({ code }) => {
        await handleVerification(code);
    }, [handleVerification]);

    return (
        <div style={{ maxWidth: 400, margin: '0 auto' }}>
            {userEmail && (
                <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
                    Код отправлен на: <strong>{userEmail}</strong>
                </Text>
            )}

            <Form form={form} onFinish={onFinish} layout="vertical">
                <Form.Item
                    name="code"
                    label="6-значный код подтверждения"
                    rules={[
                        { required: true, message: 'Введите код из письма' },
                        { pattern: /^\d{6}$/, message: 'Ровно 6 цифр' },
                        () => ({
                            validator(_, value) {
                                if (!value || /^\d{6}$/.test(value)) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('Код должен содержать ровно 6 цифр'));
                            },
                        }),
                    ]}
                    validateTrigger="onBlur"
                >
                    <Input
                        id="verificationCode"
                        placeholder="123456"
                        maxLength={6}
                        autoComplete="one-time-code"
                        inputMode="numeric"
                        pattern="\d{6}"
                    />
                </Form.Item>

                <Form.Item style={{ marginBottom: 8 }}>
                    <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={loading}
                        block
                        size="large"
                    >
                        {loading ? 'Проверка...' : 'Подтвердить'}
                    </Button>
                </Form.Item>

                <Form.Item>
                    <Button
                        onClick={handleResendCode}
                        loading={codeLoading}
                        disabled={codeLoading || countdown > 0}
                        block
                        size="large"
                    >
                        {countdown > 0
                            ? `Повторная отправка (${countdown})`
                            : codeLoading
                                ? 'Отправка...'
                                : 'Отправить код повторно'
                        }
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default VerifyForm;