// src/app/user/settings/page.tsx

'use client';

import { UserSettingsForm } from '@/components/user-settings-form';
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
	CardDescription,
} from '@/components/ui/card';

export default function UserSettingsPage() {
	return (
		<div className="container mx-auto py-10">
			<Card>
				<CardHeader>
					<CardTitle>Settings</CardTitle>
					<CardDescription>
						Update your username and email address here.
					</CardDescription>
				</CardHeader>
				<CardContent>
					<UserSettingsForm />
				</CardContent>
			</Card>
		</div>
	);
}
