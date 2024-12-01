// src/app/user/password/page.tsx

'use client';

import { UserChangePasswordForm } from '@/components/user-change-password';
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
	CardDescription,
} from '@/components/ui/card';

export default function UserChangePasswordPage() {
	return (
		<div className="container mx-auto py-10">
			<Card>
				<CardHeader>
					<CardTitle>Change Password</CardTitle>
					<CardDescription>Update your account password here.</CardDescription>
				</CardHeader>
				<CardContent>
					<UserChangePasswordForm />
				</CardContent>
			</Card>
		</div>
	);
}
