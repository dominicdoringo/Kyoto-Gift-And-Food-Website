import { Metadata } from 'next';
import UserDashboardPage from '@/components/UserDashboardPage';

export const metadata: Metadata = {
	title: 'User Dashboard',
	description: 'User dashboard for our e-commerce platform',
};

export default function UserPage() {
	return <UserDashboardPage />;
}
