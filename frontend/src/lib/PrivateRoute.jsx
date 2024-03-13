import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import Sidebar from '../components/navbar/Sidebar';
import Page from '../pages/Page';
import i18next from 'i18next';

const PrivateRoute = ({ component: Component, ...rest }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const response = await fetch('https://127.0.0.1:8080/auth/verify_token', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Token ${token}`,
                        },
                    });
                    if (response.ok) {
                        const responseData = await response.json();
                        setIsAuthenticated(true);
                        i18next.changeLanguage(responseData.language);
                        setIsAuthenticated(true);
                    } else {
                        setIsAuthenticated(false);
                    }
                } catch (error) {
                    setIsAuthenticated(false);
                }
            } else {
                setIsAuthenticated(false);
            }
        };

        verifyToken();
    }, []);

    if (isAuthenticated === null) {
        return <div>Loading...</div>;
    } else if (isAuthenticated) {
        return  <>
            <Sidebar></Sidebar>
            <Page>
                <Component {...rest} />
            </Page>
        </>
    } else {
        return  <Navigate to="/login" replace />;
    }
};

export default PrivateRoute;