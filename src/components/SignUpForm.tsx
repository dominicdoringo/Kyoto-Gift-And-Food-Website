'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useState } from 'react';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useRouter } from 'next/navigation';
import { Modal } from '@/components/ui/modal'; // Import your Modal component

// Zod schema for form validation
const signUpSchema = z.object({
	username: z
		.string()
		.min(3, { message: 'Username must be at least 3 characters' })
		.max(20, { message: 'Username must be at most 20 characters' })
		.regex(/^[a-zA-Z0-9_]+$/, {
			message: 'Username can only contain letters, numbers, and underscores',
		}),
	email: z.string().email({ message: 'Invalid email address' }),
	password: z
		.string()
		.min(8, { message: 'Password must be at least 8 characters' })
		.regex(
			/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
			{
				message:
					'Password must include uppercase, lowercase, number, and special character',
			}
		),
});

export function SignUpForm() {
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [isModalOpen, setIsModalOpen] = useState(false);
	const { toast } = useToast();
	const router = useRouter();

	// Initialize the form with zod resolver
	const form = useForm<z.infer<typeof signUpSchema>>({
		resolver: zodResolver(signUpSchema),
		defaultValues: {
			username: '',
			email: '',
			password: '',
		},
	});

	// Handle form submission
	async function onSubmit(values: z.infer<typeof signUpSchema>) {
		setIsSubmitting(true);
		try {
			// Send POST request to the API
			const response = await fetch(`${API_HOST_BASE_URL}/users/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(values),
			});

			if (response.ok) {
				// Registration successful
				toast({
					title: 'Registration Successful',
					description: 'Please verify your email to complete registration.',
				});

				// Show the verification prompt modal
				setIsModalOpen(true);
			} else {
				// Handle errors returned from the API
				const errorData = await response.json();
				toast({
					title: 'Registration Failed',
					description:
						errorData.detail || 'An error occurred during registration.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Sign up failed', error);
			toast({
				title: 'Registration Failed',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setIsSubmitting(false);
		}
	}

	return (
		<>
			<Form {...form}>
				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className="space-y-4 w-full max-w-md"
				>
					{/* Username */}
					<FormField
						control={form.control}
						name="username"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Username</FormLabel>
								<FormControl>
									<Input
										placeholder="johndoe123"
										{...field}
									/>
								</FormControl>
								<FormMessage />
							</FormItem>
						)}
					/>

					{/* Email */}
					<FormField
						control={form.control}
						name="email"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Email</FormLabel>
								<FormControl>
									<Input
										placeholder="john.doe@example.com"
										type="email"
										{...field}
									/>
								</FormControl>
								<FormMessage />
							</FormItem>
						)}
					/>

					{/* Password */}
					<FormField
						control={form.control}
						name="password"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Password</FormLabel>
								<FormControl>
									<Input
										placeholder="********"
										type="password"
										{...field}
									/>
								</FormControl>
								<FormMessage />
							</FormItem>
						)}
					/>

					{/* Submit Button */}
					<Button
						type="submit"
						className="w-full"
						disabled={isSubmitting}
					>
						{isSubmitting ? 'Signing Up...' : 'Create Account'}
					</Button>
				</form>
			</Form>

			{/* Modal Component */}
			{isModalOpen && (
				<Modal onClose={() => router.push('/sign-in')}>
					<div className="p-6">
						<h2 className="text-xl font-bold mb-4">Verify Your Email</h2>
						<p className="mb-4">
							Please complete your registration by verifying your email. We've
							sent a verification link to your email address.
						</p>
						<Button onClick={() => router.push('/sign-in')}>
							Sign In Page
						</Button>
					</div>
				</Modal>
			)}
		</>
	);
}
