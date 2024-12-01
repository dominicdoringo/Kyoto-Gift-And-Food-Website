// src/components/user-delete-account.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from '@/components/ui/form';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useAuth } from '@/context/AuthContext';
import {
	AlertDialog,
	AlertDialogTrigger,
	AlertDialogContent,
	AlertDialogHeader,
	AlertDialogTitle,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogAction,
	AlertDialogCancel,
} from '@/components/ui/alert-dialog'; // Adjust the import path as needed

// Define the form schema using Zod
const formSchema = z
	.object({
		password: z.string().min(8, {
			message: 'Password must be at least 8 characters.',
		}),
	})
	.refine((data) => data.password.trim().length > 0, {
		message: 'Password is required.',
		path: ['password'],
	});

type FormValues = z.infer<typeof formSchema>;

export function UserDeleteAccountForm() {
	const [isPending, setIsPending] = useState(false);
	const [userId, setUserId] = useState<number | null>(null);
	const { toast } = useToast();
	const router = useRouter();
	const { isLoggedIn, logout } = useAuth();

	// Get accessToken from localStorage
	const accessToken =
		typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

	const form = useForm<FormValues>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			password: '',
		},
	});

	// Fetch user data to get userId
	useEffect(() => {
		if (!accessToken) {
			router.push('/sign-in');
			return;
		}

		const fetchUserData = async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/users/me`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				});
				if (response.ok) {
					const data = await response.json();
					setUserId(data.id);
				} else {
					toast({
						title: 'Error',
						description: 'Failed to fetch user data.',
						variant: 'destructive',
					});
					router.push('/sign-in');
				}
			} catch (error) {
				console.error('Error fetching user data:', error);
				toast({
					title: 'Error',
					description: 'An unexpected error occurred.',
					variant: 'destructive',
				});
				router.push('/sign-in');
			}
		};

		fetchUserData();
	}, [accessToken, router, toast]);

	const onSubmit = async (values: FormValues) => {
		if (!accessToken || !userId) {
			toast({
				title: 'Error',
				description: 'You must be logged in to delete your account.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		setIsPending(true);

		try {
			const response = await fetch(`${API_HOST_BASE_URL}/users/${userId}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${accessToken}`,
				},
				body: JSON.stringify({
					password: values.password, // Assuming backend requires password confirmation
				}),
			});

			if (response.ok) {
				toast({
					title: 'Account Deleted',
					description: 'Your account has been successfully deleted.',
				});
				form.reset();
				logout(); // Logs out the user and redirects to sign-in
			} else {
				const errorData = await response.json();
				toast({
					title: 'Error',
					description: errorData.detail || 'Failed to delete account.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error deleting account:', error);
			toast({
				title: 'Error',
				description:
					'An unexpected error occurred while deleting your account.',
				variant: 'destructive',
			});
		} finally {
			setIsPending(false);
		}
	};

	return (
		<AlertDialog>
			<AlertDialogTrigger asChild>
				<Button variant="destructive">Delete Account</Button>
			</AlertDialogTrigger>
			<AlertDialogContent>
				<AlertDialogHeader>
					<AlertDialogTitle>Confirm Account Deletion</AlertDialogTitle>
					<AlertDialogDescription>
						Are you sure you want to delete your account? This action is
						irreversible and all your data will be permanently removed.
					</AlertDialogDescription>
				</AlertDialogHeader>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="mt-4 space-y-4"
					>
						{/* Password Confirmation Field */}
						<FormField
							control={form.control}
							name="password"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Your Password</FormLabel>
									<FormControl>
										<Input
											type="password"
											placeholder="Enter your password"
											{...field}
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>

						<AlertDialogFooter>
							<AlertDialogCancel asChild>
								<Button
									type="button"
									variant="outline"
								>
									Cancel
								</Button>
							</AlertDialogCancel>
							<AlertDialogAction asChild>
								<Button
									type="submit"
									variant="destructive"
									disabled={isPending}
								>
									{isPending ? 'Deleting...' : 'Delete Account'}
								</Button>
							</AlertDialogAction>
						</AlertDialogFooter>
					</form>
				</Form>
			</AlertDialogContent>
		</AlertDialog>
	);
}
