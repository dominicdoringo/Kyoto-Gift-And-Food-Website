// src/app/admin/products/add/page.tsx

import { Metadata } from 'next';
import AddProductPage from '@/components/AddProductPage';

export const metadata: Metadata = {
	title: 'Add New Product',
	description: 'Admin interface to add new products to the database.',
};

export default function AddProduct() {
	return <AddProductPage />;
}
