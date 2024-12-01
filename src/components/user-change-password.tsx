// src/components/user-change-password.tsx

'use client';

import { useState, useEffect } from 'react';
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

const formSchema = z
	.object({
		oldPassword: z.string().min(8, {
			message: 'Old password must be at least 8 characters.',
		}),
		newPassword: z.string().min(8, {
			message: 'New password must be at least 8 characters.',
		}),
		confirmNewPassword: z.string(),
	})
	.refine((data) => data.newPassword === data.confirmNewPassword, {
		message: 'New passwords do not match.',
		path: ['confirmNewPassword'],
	});

export function UserChangePasswordForm() {
	const [isPending, setIsPending] = useState(false);
	const { toast } = useToast();
	const router = useRouter();

	// Get accessToken from localStorage
	const accessToken =
		typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

	// Get userId from localStorage or fetch it
	const [userId, setUserId] = useState<string | null>(
		typeof window !== 'undefined' ? localStorage.getItem('userId') : null
	);

	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			oldPassword: '',
			newPassword: '',
			confirmNewPassword: '',
		},
	});

	// Fetch userId if not available
	useEffect(() => {
		if (!accessToken) {
			router.push('/sign-in');
			return;
		}

		if (!userId) {
			const fetchUserData = async () => {
				try {
					const response = await fetch(`${API_HOST_BASE_URL}/users/me`, {
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					});
					if (response.ok) {
						const data = await response.json();
						setUserId(data.id.toString());
						localStorage.setItem('userId', data.id.toString());
					} else {
						router.push('/sign-in');
					}
				} catch (error) {
					console.error('Error fetching user data:', error);
					router.push('/sign-in');
				}
			};

			fetchUserData();
		}
	}, [accessToken, router, userId]);

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		if (!accessToken || !userId) {
			toast({
				title: 'Error',
				description: 'You must be logged in to change your password.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		setIsPending(true);

		try {
			const response = await fetch(
				`${API_HOST_BASE_URL}/users/${userId}/password`,
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${accessToken}`,
					},
					body: JSON.stringify({
						old_password: values.oldPassword,
						new_password: values.newPassword,
					}),
				}
			);

			if (response.ok) {
				toast({
					title: 'Success',
					description: 'Your password has been updated.',
				});
				form.reset();
			} else {
				const errorData = await response.json();
				toast({
					title: 'Error',
					description: errorData.detail || 'Failed to update password.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error updating password:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while updating password.',
				variant: 'destructive',
			});
		} finally {
			setIsPending(false);
		}
	};

	return (
		<Form {...form}>
			<form
				onSubmit={form.handleSubmit(onSubmit)}
				className="space-y-8"
			>
				{/* Old Password Field */}
				<FormField
					control={form.control}
					name="oldPassword"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Old Password</FormLabel>
							<FormControl>
								<Input
									type="password"
									placeholder="Enter your old password"
									{...field}
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				{/* New Password Field */}
				<FormField
					control={form.control}
					name="newPassword"
					render={({ field }) => (
						<FormItem>
							<FormLabel>New Password</FormLabel>
							<FormControl>
								<Input
									type="password"
									placeholder="Enter a new password"
									{...field}
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				{/* Confirm New Password Field */}
				<FormField
					control={form.control}
					name="confirmNewPassword"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Confirm New Password</FormLabel>
							<FormControl>
								<Input
									type="password"
									placeholder="Confirm your new password"
									{...field}
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				<Button
					type="submit"
					disabled={isPending}
				>
					{isPending ? 'Updating...' : 'Change Password'}
				</Button>
			</form>
		</Form>
	);
}
