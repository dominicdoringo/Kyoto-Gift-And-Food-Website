'use client';

import React, { useState, useEffect } from 'react';
import { UserSidebar } from '@/components/user-sidebar';
import { UserDashboard } from '@/components/user-dashboard';
import { RecentOrders } from '@/components/recent-orders';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';

interface UserData {
	username: string;
	first_name: string;
	last_name: string;
	email: string;
	// Add more fields as needed
}

export default function UserDashboardPage() {
	const [userData, setUserData] = useState<UserData | null>(null);
	const { isLoggedIn } = useAuth(); // Access auth state
	const { toast } = useToast();

	useEffect(() => {
		// Fetch user data when the component mounts
		const fetchUserData = async () => {
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

		if (isLoggedIn) {
			fetchUserData();
		} else {
			// Optionally, redirect to sign-in page if not logged in
			// router.push('/sign-in');
		}
	}, [isLoggedIn, toast]);

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<UserSidebar userData={userData} />
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<div className="flex items-center justify-between space-y-2">
							<h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
						</div>
						<UserDashboard />
						<Card>
							<CardHeader>
								<CardTitle>Recent Orders</CardTitle>
								<CardDescription>
									Your order history from the past 30 days.
								</CardDescription>
							</CardHeader>
							<CardContent>
								<RecentOrders />
							</CardContent>
						</Card>
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}
