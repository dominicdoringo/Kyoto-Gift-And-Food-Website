// src/app/user/page.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';

export default function UserPage() {
	interface UserData {
		username: string;
		email: string;
		// Add more fields as needed
	}

	const [userData, setUserData] = useState<UserData | null>(null);
	const { isLoggedIn, logout } = useAuth(); // Access auth state
	const { toast } = useToast();

	const handleGetUserData = async () => {
		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'You are not logged in.',
				variant: 'destructive',
			});
			return;
		}

		try {
			const response = await fetch(`${API_HOST_BASE_URL}/users/`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data = await response.json();
				setUserData(data);
				toast({
					title: 'User Data Fetched',
					description: 'Successfully retrieved your user data.',
				});
			} else {
				toast({
					title: 'Error',
					description: 'Failed to fetch user data.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('An error occurred:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		}
	};

	useEffect(() => {
		if (!isLoggedIn) {
			// Optionally, redirect to sign-in page if not logged in
			// router.push('/sign-in');
		}
	}, [isLoggedIn]);

	return (
		<div className="p-6">
			<h1 className="text-2xl font-bold mb-4">User Page</h1>
			<p>Here I want the user data to be here</p>
			<Button
				onClick={handleGetUserData}
				className="mt-4"
			>
				Get User Data
			</Button>
			{userData && (
				<div className="mt-4">
					<p>
						<strong>Username:</strong> {userData.username}
					</p>
					<p>
						<strong>Email:</strong> {userData.email}
					</p>
					{/* Add more user information as needed */}
				</div>
			)}
		</div>
	);
}
