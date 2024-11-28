'use client';

import React, { useState } from 'react';
import { API_HOST_BASE_URL } from '@/lib/constants';

export default function UserPage() {
	interface UserData {
		username: string;
		email: string;
		// Add more fields as needed
	}

	const [userData, setUserData] = useState<UserData | null>(null);

	const handleGetUserData = async () => {
		const token = localStorage.getItem('accessToken');
		if (!token) {
			console.log('No token found');
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
			} else {
				console.log('Failed to fetch user data');
			}
		} catch (error) {
			console.error('An error occurred:', error);
		}
	};

	return (
		<div className="p-6">
			<h1 className="text-2xl font-bold mb-4">User Page</h1>
			<p>Here I want the user data to be here</p>
			<button
				onClick={handleGetUserData}
				className="px-4 py-2 bg-blue-500 text-white rounded-md"
			>
				Get User Data
			</button>
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
