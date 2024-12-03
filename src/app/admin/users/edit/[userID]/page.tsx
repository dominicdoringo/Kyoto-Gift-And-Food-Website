// src/app/admin/users/edit/[userId]/page.tsx

import EditUserPage from '@/components/EditUserPage';

interface PageProps {
	params: {
		userId: string;
	};
}

export default function EditUser({ params }: PageProps) {
	return <EditUserPage userId={params.userId} />;
}
