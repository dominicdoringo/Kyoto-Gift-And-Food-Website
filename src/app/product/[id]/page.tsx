import ProductPage from '@/components/product';

export default async function Page({ params }: { params: { id: number } }) {
	const identity = params.id;
	return <ProductPage id={identity} />;
}
