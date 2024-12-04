'use client';

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useRef } from 'react';
import { Button } from '@/components/ui/button';
import { FeaturedItemCard } from '@/components/ui/featured-item-card';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { Product } from '@/lib/types';

export function ListItems({ title = '', categoryType = 'snacks' }) {
	const scrollContainerRef = useRef<HTMLDivElement>(null);

	const [products, setProducts] = useState<Product[]>([]);

	useEffect(() => {
		const fetchProductItems = async () => {
			try {
				const response = await fetch(
					`${API_HOST_BASE_URL}/products?category=${categoryType}`
				);
				if (response.ok) {
					const data: Product[] = await response.json();
					const filteredProducts = data.filter(
						(product) => product.category === categoryType
					);
					const productsWithImages = filteredProducts.map((product) => ({
						...product,
						imageUrl:
							product.imageUrl ||
							'https://m.media-amazon.com/images/I/91gJhDXaehL._AC_UF894,1000_QL80_.jpg', // Use imageUrl from backend or fallback
					}));
					setProducts(productsWithImages);
				} else {
					console.error('Failed to fetch product items');
				}
			} catch (error) {
				console.error('Error fetching product items:', error);
			}
		};

		fetchProductItems();
	}, []);

	const scroll = (direction: 'left' | 'right') => {
		if (scrollContainerRef.current) {
			const scrollAmount = 330; // Card width + gap
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
				<h2 className="text-4xl font-bold text-center mb-8">{title}</h2>
				<div className="relative">
					<div
						ref={scrollContainerRef}
						className="flex gap-6 overflow-x-hidden scroll-smooth pb-4"
					>
						{products.map((item, index) => (
							<FeaturedItemCard
								key={index}
								{...item}
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
