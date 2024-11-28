// src/context/AuthContext.tsx

'use client';

import React, { createContext, useState, useEffect, useContext } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from '@/hooks/use-toast';

interface AuthContextProps {
	isLoggedIn: boolean;
	login: (token: string) => void;
	logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
	children,
}) => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const router = useRouter();
	const { toast } = useToast();

	useEffect(() => {
		const token = localStorage.getItem('accessToken');
		setIsLoggedIn(!!token);
	}, []);

	const login = (token: string) => {
		localStorage.setItem('accessToken', token);
		setIsLoggedIn(true);
		toast({
			title: 'Login Successful',
			description: 'You have been successfully logged in.',
		});
		router.push('/user');
	};

	const logout = () => {
		localStorage.removeItem('accessToken');
		setIsLoggedIn(false);
		toast({
			title: 'Logged Out',
			description: 'You have been successfully logged out.',
		});
		router.push('/sign-in');
	};

	return (
		<AuthContext.Provider value={{ isLoggedIn, login, logout }}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const context = useContext(AuthContext);
	if (!context) {
		throw new Error('useAuth must be used within an AuthProvider');
	}
	return context;
};
