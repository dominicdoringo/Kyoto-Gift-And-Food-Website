// src/app/admin/products/edit/[productId]/page.tsx

import EditProductPage from '@/components/EditProductPage';

export default function EditProduct({
	params,
}: {
	params: { productId: string };
}) {
	return <EditProductPage productId={params.productId} />;
}
