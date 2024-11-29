// src/components/EditUserPage.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { AdminSidebar } from '@/components/admin-sidebar';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';

interface User {
	id: number;
	username: string;
	email: string;
	is_admin: boolean;
	is_active: boolean;
	// Include other fields as needed
}

export default function EditUserPage({ userId }: { userId: string }) {
	const [user, setUser] = useState<User | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [userData, setUserData] = useState<any>(null); // For admin sidebar
	const { isLoggedIn, isAdmin } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	useEffect(() => {
		if (!isLoggedIn) {
			router.replace('/sign-in');
		} else if (!isAdmin) {
			router.replace('/user'); // Redirect non-admin users
		} else {
			fetchUserData(); // Fetch admin user data for the sidebar
			fetchUser(); // Fetch the user to edit
		}
	}, [isLoggedIn, isAdmin, router]);

	const fetchUserData = async () => {
		// Similar to previous fetchUserData implementation
	};

	const fetchUser = async () => {
		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'No access token found.',
				variant: 'destructive',
			});
			router.replace('/sign-in');
			return;
		}
		try {
			const response = await fetch(
				`${API_HOST_BASE_URL}/admin/users/${userId}`,
				{
					method: 'GET',
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);

			if (response.ok) {
				const data = await response.json();
				setUser(data);
			} else {
				const errorText = await response.text();
				console.error('Failed to fetch user:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to fetch user.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching user:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setLoading(false);
		}
	};

	const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (user) {
			setUser({ ...user, [e.target.name]: e.target.value });
		}
	};

	const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (user) {
			setUser({ ...user, [e.target.name]: e.target.checked });
		}
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!user) return;

		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'No access token found.',
				variant: 'destructive',
			});
			router.replace('/sign-in');
			return;
		}

		try {
			const response = await fetch(
				`${API_HOST_BASE_URL}/admin/users/${userId}`,
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`,
					},
					body: JSON.stringify({
						username: user.username,
						email: user.email,
						is_active: user.is_active,
						// Include other fields as needed
					}),
				}
			);

			if (response.ok) {
				toast({
					title: 'Success',
					description: 'User updated successfully.',
				});
				router.push('/admin/users');
			} else {
				const errorText = await response.text();
				console.error('Failed to update user:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to update user.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error updating user:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		}
	};

	if (loading || !user) {
		return <p>Loading...</p>;
	}

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<AdminSidebar userData={userData} />
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<h1 className="text-2xl font-bold mb-4">Edit User</h1>
						<form
							onSubmit={handleSubmit}
							className="space-y-4"
						>
							<div>
								<label className="block text-sm font-medium">Username</label>
								<input
									type="text"
									name="username"
									value={user.username}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Email</label>
								<input
									type="email"
									name="email"
									value={user.email}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div className="flex items-center">
								<input
									type="checkbox"
									name="is_active"
									checked={user.is_active}
									onChange={handleCheckboxChange}
									className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
								/>
								<label className="ml-2 block text-sm font-medium">
									Is Active
								</label>
							</div>
							{/* Add other fields as needed */}
							<button
								type="submit"
								className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
							>
								Save Changes
							</button>
						</form>
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}
