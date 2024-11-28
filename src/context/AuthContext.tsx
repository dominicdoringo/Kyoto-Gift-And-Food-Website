'use client';

import React, { createContext, useState, useEffect, useContext } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';

interface AuthContextProps {
	isLoggedIn: boolean;
	isAdmin: boolean; // Add isAdmin
	login: (token: string) => void;
	logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
	children,
}) => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [isAdmin, setIsAdmin] = useState(false); // State for admin role
	const router = useRouter();
	const { toast } = useToast();

	useEffect(() => {
		const token = localStorage.getItem('accessToken');
		setIsLoggedIn(!!token);
		if (token) {
			fetchUserRole(token);
		}
	}, []);

	const fetchUserRole = async (token: string) => {
		try {
			const response = await fetch(`${API_HOST_BASE_URL}/users/me`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});
			if (response.ok) {
				const userData = await response.json();
				setIsAdmin(userData.is_admin); // Set isAdmin based on user data
			} else {
				// Handle error, possibly logout user
				logout();
			}
		} catch (error) {
			console.error('Failed to fetch user role:', error);
			// Handle error, possibly logout user
			logout();
		}
	};

	const login = async (token: string) => {
		localStorage.setItem('accessToken', token);
		setIsLoggedIn(true);
		await fetchUserRole(token); // Fetch user role after login
		toast({
			title: 'Login Successful',
			description: 'You have been successfully logged in.',
		});
		router.push(isAdmin ? '/admin' : '/user');
	};

	const logout = () => {
		localStorage.removeItem('accessToken');
		setIsLoggedIn(false);
		setIsAdmin(false);
		toast({
			title: 'Logged Out',
			description: 'You have been successfully logged out.',
		});
		router.push('/sign-in');
	};

	return (
		<AuthContext.Provider value={{ isLoggedIn, isAdmin, login, logout }}>
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
