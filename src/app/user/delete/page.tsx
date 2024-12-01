// src/app/user/delete/page.tsx

'use client';

import React from 'react';
import { UserDeleteAccountForm } from '@/components/user-delete-account';
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
	CardDescription,
} from '@/components/ui/card';

export default function DeleteAccountPage() {
	return (
		<div className="container mx-auto py-10">
			<Card className="max-w-lg mx-auto">
				<CardHeader>
					<CardTitle>Delete Account</CardTitle>
					<CardDescription>
						Permanently delete your account. This action cannot be undone.
					</CardDescription>
				</CardHeader>
				<CardContent>
					<UserDeleteAccountForm />
				</CardContent>
			</Card>
		</div>
	);
}
