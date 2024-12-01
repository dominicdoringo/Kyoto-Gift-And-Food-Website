// src/components/user-settings-form.tsx

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
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from '@/components/ui/form';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';
import { API_HOST_BASE_URL } from '@/lib/constants';

const formSchema = z.object({
	username: z.string().min(3, {
		message: 'Username must be at least 3 characters.',
	}),
	email: z.string().email({
		message: 'Please enter a valid email address.',
	}),
});

export function UserSettingsForm() {
	const [isPending, setIsPending] = useState(false);
	const [userId, setUserId] = useState<number | null>(null);

	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			username: '',
			email: '',
		},
	});

	const { toast } = useToast();
	const router = useRouter();

	// Get accessToken from localStorage
	const accessToken =
		typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

	// useEffect to fetch user data
	useEffect(() => {
		if (!accessToken) {
			// Redirect to login page
			router.push('/sign-in');
			return;
		}

		// Fetch user data from /users/me
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
					// Set form default values
					form.reset({
						username: data.username,
						email: data.email,
					});
				} else {
					// Handle error
					const errorData = await response.json();
					toast({
						title: 'Error',
						description: errorData.detail || 'Failed to fetch user data',
						variant: 'destructive',
					});
					router.push('/sign-in');
				}
			} catch (error) {
				console.error('Error fetching user data:', error);
				toast({
					title: 'Error',
					description: 'An unexpected error occurred while fetching user data.',
					variant: 'destructive',
				});
				router.push('/sign-in');
			}
		};

		fetchUserData();
	}, [accessToken, form, router, toast]);

	const onSubmit = async (values: z.infer<typeof formSchema>) => {
		if (!accessToken || !userId) {
			toast({
				title: 'Error',
				description: 'You must be logged in to update settings.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		setIsPending(true);

		try {
			const response = await fetch(`${API_HOST_BASE_URL}/users/${userId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${accessToken}`,
				},
				body: JSON.stringify(values),
			});

			if (response.ok) {
				const data = await response.json();
				toast({
					title: 'Success',
					description: 'Your settings have been updated.',
				});
				// Optionally, update userData in AuthContext or localStorage
			} else {
				const errorData = await response.json();
				toast({
					title: 'Error',
					description: errorData.detail || 'Failed to update settings.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error updating user settings:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while updating settings.',
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
				<FormField
					control={form.control}
					name="username"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Username</FormLabel>
							<FormControl>
								<Input
									placeholder="johndoe"
									{...field}
								/>
							</FormControl>
							<FormDescription>
								This is your public display name.
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Email</FormLabel>
							<FormControl>
								<Input
									placeholder="john@example.com"
									{...field}
								/>
							</FormControl>
							<FormDescription>
								This is the email associated with your account.
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>
				<Button
					type="submit"
					disabled={isPending}
				>
					{isPending ? 'Updating...' : 'Update Settings'}
				</Button>
			</form>
		</Form>
	);
}
