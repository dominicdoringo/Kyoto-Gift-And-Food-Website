'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';

// Zod schema for form validation
const loginSchema = z.object({
	username: z
		.string()
		.min(3, { message: 'Username must be at least 3 characters long' }),
	password: z
		.string()
		.min(3, { message: 'Password must be at least 8 characters long' }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

// Simulated server action (in a real app, this would be in a separate file)
async function loginUser(data: LoginFormValues) {
	const response = await fetch(`${API_HOST_BASE_URL}/users/token`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams(data).toString(),
	});

	if (response.ok) {
		const result = await response.json();
		console.log(result);
		return { success: true, token: result.access_token };
	}

	throw new Error('Invalid credentials');
}

export function LoginForm() {
	const [isLoading, setIsLoading] = useState(false);
	const { toast } = useToast();
	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<LoginFormValues>({
		resolver: zodResolver(loginSchema),
	});

	const onSubmit = async (data: LoginFormValues) => {
		setIsLoading(true);
		try {
			const result = await loginUser(data);
			if (result.success) {
				// Save the token to localStorage
				localStorage.setItem('accessToken', result.token);
				toast({
					title: 'Login Successful',
					description: 'You have been successfully logged in.',
				});
			}
		} catch (error) {
			toast({
				title: 'Login Failed',
				description: 'Invalid username or password.',
				variant: 'destructive',
			});
			console.log(error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<Card className="w-[350px]">
			<CardHeader>
				<CardTitle>Login</CardTitle>
				<CardDescription>
					Enter your credentials to access your account.
				</CardDescription>
			</CardHeader>
			<CardContent>
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="grid w-full items-center gap-4">
						<div className="flex flex-col space-y-1.5">
							<Label htmlFor="username">Username</Label>
							<Input
								id="username"
								{...register('username')}
							/>
							{errors.username && (
								<p className="text-sm text-red-500">
									{errors.username.message}
								</p>
							)}
						</div>
						<div className="flex flex-col space-y-1.5">
							<Label htmlFor="password">Password</Label>
							<Input
								id="password"
								type="password"
								{...register('password')}
							/>
							{errors.password && (
								<p className="text-sm text-red-500">
									{errors.password.message}
								</p>
							)}
						</div>
					</div>
					<CardFooter className="flex justify-between mt-4 px-0">
						<Button
							type="submit"
							disabled={isLoading}
						>
							{isLoading ? 'Logging in...' : 'Login'}
						</Button>
					</CardFooter>
				</form>
			</CardContent>
		</Card>
	);
}
