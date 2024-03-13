import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Validation from '../../components/validation/Validation';

const Register = () => {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');


    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                const response = await fetch('https://127.0.0.1:8080/auth/verify_token', {
                    method: 'GET',
                    headers: {
                    'Authorization': `Token ${token}`,
                    },
                });
                if (response.ok) {
                    navigate('/');
                }
            }
        }
        verifyToken();
    });

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('https://127.0.0.1:8080/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    email: email,
                }),
            });

            if (response.ok) {
                navigate("/");
            } else {
                setError("");
                const errorMessage = await response.json();
                let res = ""
                if (errorMessage.username) {
                    res += errorMessage.username + " "
                }
    
                if (errorMessage.password) {
                    res += errorMessage.password + " "
                }
                setError(res);
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className='login-page'>
            <form className='login-form' onSubmit={handleRegister}>
                { error ? <Validation message={error}></Validation> : null }
                <input
                    required="required" 
                    className='login-input'
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    autoComplete='username'
                />
                <input
                    required="required" 
                    className='login-input'
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete=''
                />
                <input
                    required="required" 
                    className='login-input'
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete='current-password'
                />
                <button type="submit" className='login-button'>Register</button>
            </form>
        </div>
    );
};

export default Register;