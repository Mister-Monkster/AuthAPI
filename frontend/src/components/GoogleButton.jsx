import React, { useState } from 'react';
import { Button, Alert } from 'antd';
import { GoogleOutlined } from '@ant-design/icons';
import axios from "axios";

const GoogleOauthButton = () => {
    const [error, setError] = useState(null);
    axios.defaults.withCredentials = true;
    const handleGoogleLogin = () => {
        setError(null);
        window.location.href = 'http://localhost:8000/google';
    };

    return (
        <div>
            <Button type="primary" onClick={handleGoogleLogin} icon={<GoogleOutlined />}>
                Войти через Google
            </Button>
            {error && <Alert message={error} type="error" showIcon />}
        </div>
    );
};

export default GoogleOauthButton;