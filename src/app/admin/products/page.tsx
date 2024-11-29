// src/app/admin/products/page.tsx

import { Metadata } from 'next';
import AdminProductsPage from '@/components/AdminProductsPage';

export const metadata: Metadata = {
	title: 'Manage Products',
};

export default function AdminProducts() {
	return <AdminProductsPage />;
}
