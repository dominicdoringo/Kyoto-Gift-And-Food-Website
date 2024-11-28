// src/app/admin/users/page.tsx

import { Metadata } from 'next';
import AdminUsersPage from '@/components/AdminUsersPage';

export const metadata: Metadata = {
	title: 'Manage Users',
};

export default function AdminUsers() {
	return <AdminUsersPage />;
}
