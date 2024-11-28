import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export function withAdminAuth(WrappedComponent: React.ComponentType<any>) {
	return function AdminProtected(props: any) {
		const { isLoggedIn, isAdmin } = useAuth();
		const router = useRouter();

		React.useEffect(() => {
			if (!isLoggedIn || !isAdmin) {
				router.replace('/sign-in');
			}
		}, [isLoggedIn, isAdmin, router]);

		if (!isLoggedIn || !isAdmin) {
			return null; // Optionally render a loading indicator
		}

		return <WrappedComponent {...props} />;
	};
}
