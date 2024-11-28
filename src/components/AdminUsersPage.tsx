// src/components/AdminUsersPage.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { AdminSidebar } from '@/components/admin-sidebar';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { UsersTable } from '@/components/UsersTable';
import { useRouter } from 'next/navigation';

interface User {
	id: number;
	username: string;
	email: string;
	is_admin: boolean;
	created_at: string;
}

interface UserData {
	username: string;
	email: string;
	// Add other fields as needed
}

export default function AdminUsersPage() {
	const [users, setUsers] = useState<User[]>([]);
	const [userData, setUserData] = useState<UserData | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const { isLoggedIn, isAdmin } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	useEffect(() => {
		if (!isLoggedIn) {
			router.replace('/sign-in');
		} else if (!isAdmin) {
			router.replace('/user'); // Redirect non-admin users
		} else {
			fetchUserData(); // Fetch user data for the sidebar
			fetchUsers(); // Fetch the list of users
		}
	}, [isLoggedIn, isAdmin, router]);

	const fetchUserData = async () => {
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
			const response = await fetch(`${API_HOST_BASE_URL}/users/me`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data = await response.json();
				setUserData(data);
			} else {
				const errorText = await response.text();
				console.error('Failed to fetch user data:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to fetch user data.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching user data:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		}
	};

	const fetchUsers = async () => {
		setLoading(true);
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
			const response = await fetch(`${API_HOST_BASE_URL}/admin/users`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data: User[] = await response.json();
				setUsers(data);
			} else {
				const errorText = await response.text();
				console.error('Failed to fetch users:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to fetch users.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching users:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setLoading(false);
		}
	};

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<AdminSidebar userData={userData} />
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<h1 className="text-2xl font-bold mb-4">Manage Users</h1>
						{loading ? <p>Loading users...</p> : <UsersTable users={users} />}
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}
