import ProductPage from '@/components/product';
import { getProductById } from '@/api/api';

export default async function Page({ params }: { params: { id: string } }) {
	const product = await getProductById(params.id);

	if (!product) {
		return <div>Product not found</div>;
	}

	return <ProductPage product={product} />;
}
