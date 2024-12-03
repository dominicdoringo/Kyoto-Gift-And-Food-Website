'use client';

import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useRef, useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { FeaturedItemCard } from '@/components/ui/featured-item-card';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { Product } from '@/lib/types';

export function FeaturedItems() {
	const [featuredItems, setFeaturedItems] = useState<Product[]>([]);
	const scrollContainerRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		const fetchFeaturedItems = async () => {
			try {
				const response = await fetch(
					`${API_HOST_BASE_URL}/products?featured=true`
				);
				if (response.ok) {
					const data: Product[] = await response.json();
					const productsWithImages = data.map((product) => ({
						...product,
						imageUrl:
							product.imageUrl ||
							'https://m.media-amazon.com/images/I/91gJhDXaehL._AC_UF894,1000_QL80_.jpg', // Use imageUrl from backend or fallback
					}));
					setFeaturedItems(productsWithImages);
				} else {
					console.error('Failed to fetch featured items');
				}
			} catch (error) {
				console.error('Error fetching featured items:', error);
			}
		};

		fetchFeaturedItems();
	}, []);

	const scroll = (direction: 'left' | 'right') => {
		if (scrollContainerRef.current) {
			const scrollAmount = 330;
			const scrollLeft = scrollContainerRef.current.scrollLeft;
			const newScrollLeft =
				direction === 'left'
					? scrollLeft - scrollAmount
					: scrollLeft + scrollAmount;

			scrollContainerRef.current.scrollTo({
				left: newScrollLeft,
				behavior: 'smooth',
			});
		}
	};

	return (
		<section className="py-12 px-6">
			<div className="max-w-7xl mx-auto">
				<h2 className="text-4xl font-bold text-center mb-8">Featured Items</h2>
				<div className="relative">
					<div
						ref={scrollContainerRef}
						className="flex gap-6 overflow-x-hidden scroll-smooth pb-4"
					>
						{featuredItems.map((item) => (
							<FeaturedItemCard
								key={item.id}
								id={item.id} // Pass the product ID
								name={item.name}
								price={item.price}
								description={item.description || ''}
								imageUrl={item.imageUrl} // Directly use imageUrl from backend
								category={item.category}
								stock={item.stock}
								featured={item.featured}
								created_at={item.created_at}
							/>
						))}
					</div>
					<Button
						variant="outline"
						size="icon"
						className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 bg-background shadow-lg"
						onClick={() => scroll('left')}
					>
						<ChevronLeft className="h-4 w-4" />
					</Button>
					<Button
						variant="outline"
						size="icon"
						className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 bg-background shadow-lg"
						onClick={() => scroll('right')}
					>
						<ChevronRight className="h-4 w-4" />
					</Button>
				</div>
			</div>
		</section>
	);
}
