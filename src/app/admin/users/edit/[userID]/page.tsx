// src/app/admin/users/edit/[userId]/page.tsx

import EditUserPage from '@/components/EditUserPage';

export default function EditUser({ params }: { params: { userId: string } }) {
	return <EditUserPage userId={params.userId} />;
}
