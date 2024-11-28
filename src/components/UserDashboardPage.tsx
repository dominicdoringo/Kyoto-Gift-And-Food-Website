'use client';

import React, { useState, useEffect } from 'react';
import { UserSidebar } from '@/components/user-sidebar';
import { AdminSidebar } from '@/components/admin-sidebar';
import { UserDashboard } from '@/components/user-dashboard';
import { AdminDashboard } from '@/components/admin-dashboard';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useRouter } from 'next/navigation';

interface UserData {
	username: string;
	email: string;
	// Add more fields as needed
}

export default function UserDashboardPage() {
	const [userData, setUserData] = useState<UserData | null>(null);
	const { isLoggedIn, isAdmin } = useAuth(); // Access isAdmin
	const { toast } = useToast();
	const router = useRouter();

	useEffect(() => {
		if (!isLoggedIn) {
			router.push('/sign-in');
			return;
		}

		const token = localStorage.getItem('accessToken');
		if (token) {
			fetchUserData(token);
		}
	}, [isLoggedIn, router]);

	const fetchUserData = async (token: string) => {
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

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				{isAdmin ? (
					<AdminSidebar userData={userData} />
				) : (
					<UserSidebar userData={userData} />
				)}
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<div className="flex items-center justify-between space-y-2">
							<h2 className="text-3xl font-bold tracking-tight">
								{isAdmin ? 'Admin Dashboard' : 'Dashboard'}
							</h2>
						</div>
						{isAdmin ? <AdminDashboard /> : <UserDashboard />}
						{/* ... Additional content ... */}
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}
